# your_app/utils/card_code_generator.py
import uuid
from django.db import transaction
from api.models import Card


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

