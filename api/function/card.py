# your_app/utils/card_code_generator.py
import uuid
from django.db import transaction
from django.forms import model_to_dict
from django.utils import timezone

from api.models import Card, CustomUser
from api.selfUtils import result


# 单生成卡密
def generate_card_codes(count: int, check_unique: bool = True) -> list[str]:
    """
    生成指定数量的卡密（基于 UUIDv4）

    :param count: 需要生成的卡密数量
    :param check_unique: 是否校验数据库唯一性（默认开启）
    :return: 生成的卡密列表（去短横线+大写）
    """
    generated_codes = []

    with transaction.atomic():  # 事务内查询，避免并发冲突
        for _ in range(count):
            # 生成 UUIDv4 并格式化为 32 位大写字符串（去短横线）
            raw_code = str(uuid.uuid4()).replace('-', '').upper()

            # 校验数据库唯一性（可选）
            if check_unique:
                # 循环直到生成未使用的卡密（理论上几乎不会重复）
                while Card.objects.filter(key=raw_code).exists():
                    raw_code = str(uuid.uuid4()).replace('-', '').upper()

            generated_codes.append(raw_code)

    return generated_codes

#将卡密存入数据库
def store_card_codes(codes: list[str], card_type: str="hour") -> None:
    """
    将生成的卡密批量存入数据库（自动处理过期时间和状态）

    :param codes: 卡密字符串列表（如 ["CODE001", "CODE002"]）
    :param card_type: 卡类型（对应 Card 模型的 card_type 字段，如 "day"/"month" 等）
    :return: None
    """
    # 预处理每个卡密实例（触发自定义逻辑）
    card_objects = []
    for code in codes:
        # 创建未保存的 Card 实例（不设置 expired_time，由后续逻辑自动计算）
        card = Card(
            key=code,
            card_type=card_type,
            status="unused",  # 初始状态为未使用
            created_time=timezone.now(),
        )

        # 手动触发自定义逻辑（与 save 方法中的逻辑一致）
        # 1. 自动计算过期时间（仅非永久卡且未手动设置时）
        if not card.expired_time and card_type != "permanent":
            card.expired_time = card.calculate_expiration()  # 调用模型中的计算方法

        # 2. 自动更新状态（根据过期时间或卡类型）
        card.update_status()  # 调用模型中的状态更新方法

        card_objects.append(card)

    # 批量插入数据库（忽略重复冲突）
    Card.objects.bulk_create(
        card_objects,
        ignore_conflicts=True  # 若 key 是唯一字段，重复时跳过（根据业务需求调整）
    )


def validate_card(key):
    """
    验证卡密有效性

    Args:
        code: 卡密字符串

    Returns:
        (状态码, 消息, 卡密对象)
    """
    try:
        card = Card.objects.get(key=key)
    except Card.DoesNotExist:
        return result.fail("卡密不存在")

    if card.status == "used":
        return result.fail("卡密已使用")

    if timezone.now() > card.expire_time or card.status == "expired":
        return result.fail("卡密已过期")

    return result.success("卡密有效,"+model_to_dict(card))

def use_card(key,user:CustomUser):
    """
    验证卡密有效性

    Args:
        code: 卡密字符串
        user: 使用卡密的用户对象

    Returns:
        (状态码, 消息, 卡密对象)
    """
    try:
        card = Card.objects.get(key=key)
    except Card.DoesNotExist:
        return result.fail("卡密不存在")

    if card.status == "used":
        return result.fail("卡密已使用")

    if timezone.now() > card.expire_time or card.status == "expired":
        return result.fail("卡密已过期")

    user = CustomUser.objects.get(id=user.id)
    if not card.expired_time and card.card_type != "permanent":
        card.expired_time = card.calculate_expiration()
        card.status = "used"
        now_time = timezone.now()
        card.used_time = now_time
        user.vip_time = now_time
        card.save()
        user.save()
    return result.success(f"卡密已使用,到期时间：{card.expired_time}")