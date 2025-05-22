from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # 新增字段示例：手机号（允许为空）
    vip_time = models.CharField(
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
        blank=False,
        null=False,
        db_index=True,
    )
    # 登录IP 地址（自动校验 IPv4/IPv6 格式，推荐使用）
    regisiter_ip = models.GenericIPAddressField(
        verbose_name="注册IP地址",
        help_text="请输入设备的 IP 地址（支持 IPv4/IPv6，如 192.168.1.1 或 2001:db8::1）",
        protocol="both",
        blank=False,
        null=False,
        db_index=True,
    )

    # 可选：重写 __str__ 方法（非必需）
    def __str__(self):
        return self.username
