from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    USER_LEVEL_CHOICES = [
        (0, '封号'),
        (1, '普通用户'),
        (2, '高级用户'),
        (3, '管理员'),
    ]

    vip_time = models.DateTimeField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name="VIP到期时间",
        help_text="请输入格式为 'YYYY-MM-DD HH:MM' 的日期时间（例如：2025-05-21 14:30）",
    )
    device = models.CharField(
        max_length=20,
        verbose_name="设备号",
        help_text="请输入设备名称（例如：iPhone 12）",
    )
    # 注册IP 地址（自动校验 IPv4/IPv6 格式，推荐使用）
    login_ip = models.GenericIPAddressField(
        verbose_name="登录IP地址",
        help_text="请输入设备的 IP 地址（支持 IPv4/IPv6，如 192.168.1.1 或 2001:db8::1）",
        protocol="both",
        null=True,      # 允许数据库中该字段为 NULL
        blank=True,     # 允许表单验证时该字段为空
        db_index=True,
    )
    # 登录IP 地址（自动校验 IPv4/IPv6 格式，推荐使用）
    regisiter_ip = models.GenericIPAddressField(
        verbose_name="注册IP地址",
        help_text="请输入设备的 IP 地址（支持 IPv4/IPv6，如 192.168.1.1 或 2001:db8::1）",
        protocol="both",
        null=True,      # 允许数据库中该字段为 NULL
        blank=True,     # 允许表单验证时该字段为空
        db_index=True,
    )
    # 用户等级
    user_level = models.PositiveSmallIntegerField(
        default=1,
        choices=USER_LEVEL_CHOICES,  # 限制只能选枚举值
        verbose_name='用户等级',
        help_text='0-封号 | 1-普通用户 | 2-高级用户 | 3-管理员'
    )
    user_code = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="用户编码"
    )

    # 上级邀请码（改为普通整数字段，不使用外键约束）
    invited_parent = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name="上级邀请码"
    )
    # 可选：重写 __str__ 方法（非必需）
    def __str__(self):
        return self.username
    def clean(self):
        """自定义校验：封号用户（user_level=0）禁止登录"""
        if self.user_level == 0 and self.is_active:
            # 若用户被标记为封号但is_active仍为True，抛出校验错误
            raise ValidationError("封号用户必须禁用登录权限（请取消勾选'活跃'状态）")

    def save(self, *args, **kwargs):
        """保存时自动同步封号状态与登录权限"""
        if self.user_level == 0:
            self.is_active = False  # 封号用户强制禁用登录
        super().save(*args, **kwargs)

class Card(models.Model):
    # 卡密类型选项（新增时长类型）
    CARD_TYPE_CHOICES = [
        ('hour', '小时卡'),
        ('day', '天卡'),
        ('week', '周卡'),
        ('month', '月卡'),
        ('year', '年卡'),
        ('permanent', '永久卡'),
    ]

    # 使用状态选项
    USE_STATUS_CHOICES = [
        ('unused', '未使用'),
        ('used', '已使用'),
        ('expired', '已过期'),
    ]

    # 卡密字段（增加复杂度）
    key = models.CharField(
        '卡密',
        max_length=50,
        unique=True,
        db_index=True,
        help_text='推荐使用UUID生成16位以上复杂字符串'
    )

    # 卡密类型（新增时长逻辑）
    card_type = models.CharField(
        '类型',
        max_length=20,
        choices=CARD_TYPE_CHOICES,
        default='day'
    )

    # 时间相关字段
    created_time = models.DateTimeField(
        '创建时间',
        #auto_now_add=True
    )
    expired_time = models.DateTimeField(
        '过期时间',
        null=True,
        blank=True,
        help_text='留空时根据卡类型自动计算'
    )
    used_time = models.DateTimeField(
        '使用时间',
        null=True,
        blank=True
    )

    # 用户关联字段
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_cards',
        verbose_name='使用者'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_cards',
        verbose_name='创建者'
    )

    # 状态管理字段
    status = models.CharField(
        '状态',
        max_length=10,
        choices=USE_STATUS_CHOICES,
        default='unused',
        db_index=True
    )

    class Meta:
        verbose_name = '卡密'
        verbose_name_plural = '卡密管理'
        ordering = ['-created_time']
        indexes = [
            models.Index(fields=['card_type', 'status']),
            models.Index(fields=['creator', 'user']),
        ]

    def __str__(self):
        return f"{self.get_card_type_display()} - {self.key}"

    def clean(self):
        """数据验证"""
        # 永久卡必须没有过期时间
        if self.card_type == 'permanent' and self.expired_time:
            raise ValidationError("永久卡不能设置过期时间")

        # 非永久卡需要过期时间
        if self.card_type != 'permanent' and not self.expired_time:
            raise ValidationError("请设置过期时间或选择永久卡")

    def save(self, *args, **kwargs):
        """自动处理逻辑"""
        # 自动计算过期时间（如果未设置）
        if not self.expired_time and self.card_type != 'permanent':
            self.expired_time = self.calculate_expiration()

        # 自动更新状态
        self.update_status()

        super().save(*args, **kwargs)

    def calculate_expiration(self):
        """根据卡类型和创建时间计算过期时间"""
        duration_map = {
            'hour': timezone.timedelta(hours=1),  # 示例：1小时有效（根据业务调整）
            'day': timezone.timedelta(days=1),  # 1天有效
            'week': timezone.timedelta(weeks=1),  # 1周有效
            'month': timezone.timedelta(days=30),  # 30天（简化处理）
            'year': timezone.timedelta(days=365),  # 365天
        }
        # 从 duration_map 中获取 timedelta（默认 0 时长）
        duration = duration_map.get(self.card_type, timezone.timedelta())
        # created_time 已由 auto_now_add 自动填充，不会为 None
        return timezone.now() + duration

    def calculate_duration(self):
        """根据卡类型和创建时间计算过期时间"""
        duration_map = {
            'hour': timezone.timedelta(hours=1),  # 示例：1小时有效（根据业务调整）
            'day': timezone.timedelta(days=1),  # 1天有效
            'week': timezone.timedelta(weeks=1),  # 1周有效
            'month': timezone.timedelta(days=30),  # 30天（简化处理）
            'year': timezone.timedelta(days=365),  # 365天
        }
        # 从 duration_map 中获取 timedelta（默认 0 时长）
        duration = duration_map.get(self.card_type, timezone.timedelta())
        return duration

    def update_status(self):
        """更新卡状态"""
        now = timezone.now()

        if self.status == 'used':
            return

        if self.expired_time and now > self.expired_time:
            self.status = 'expired'
        else:
            self.status = 'unused'

    @property
    def duration(self):
        """获取有效时长（人类可读）"""
        if self.card_type == 'permanent':
            return '永久有效'

        durations = {
            'hour': '小时',
            'day': '天',
            'week': '周',
            'month': '月',
            'year': '年'
        }
        return f"{durations.get(self.card_type, '')}卡"


    @property
    def is_valid(self):
        """是否有效"""
        return self.status == 'unused' and not self.is_expired

    @property
    def is_expired(self):
        """是否过期"""
        if self.card_type == 'permanent':
            return False
        return timezone.now() > self.expired_time if self.expired_time else False

