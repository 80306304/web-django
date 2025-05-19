from rest_framework.response import Response
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from DjangoProject1.settings import RSA_PUBLIC_KEY, RSA_PRIVATE_KEY

AES_SECRET_KEY = settings.AES_SECRET_KEY.encode('utf-8')  # 必须为 16/24/32 字节长度
AES_IV = settings.AES_IV.encode('utf-8')  # 必须为 16 字节长度

class result:
    """
    统一响应格式封装类
    支持：成功响应、错误响应、自定义状态码
    示例：result.success(data={"name": "张三"}) → {"code": 200, "msg": "操作成功", "data": {"name": "张三"}}
    """
    SUCCESS_CODE = 200
    ERROR_CODE = 400
    DEFAULT_SUCCESS_MSG = "操作成功"
    DEFAULT_ERROR_MSG = "操作失败"

    @classmethod
    def success(cls, data=None, msg: str = None, code: int = None) -> Response:
        """
        成功响应
        :param data: 响应数据（可选）
        :param msg: 自定义提示信息（可选）
        :param code: 自定义状态码（可选，默认200）
        """
        response_data = {
            "code": code or cls.SUCCESS_CODE,
            "msg": msg or cls.DEFAULT_SUCCESS_MSG,
            "data": data if data is not None else {}
        }
        return Response(response_data)

    @classmethod
    def fail(cls, msg: str = None, code: int = None, details: dict = None) -> Response:
        """
        错误响应
        :param msg: 错误提示信息（可选，默认"操作失败"）
        :param code: 自定义错误码（可选，默认400）
        :param details: 错误详情（可选，用于传递具体错误信息如参数校验结果）
        """
        response_data = {
            "code": code or cls.ERROR_CODE,
            "msg": msg or cls.DEFAULT_ERROR_MSG,
            "data": {}
        }
        if details:
            response_data["data"]["details"] = details
        return Response(response_data)

def aes_encrypt(data: str) -> str:
    """AES 加密（CBC 模式）"""
    data_bytes = data.encode('utf-8')
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
    encrypted_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def aes_decrypt(encrypted_data: str) -> str:
    """AES 解密（CBC 模式）"""
    encrypted_bytes = base64.b64decode(encrypted_data)
    cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    return decrypted_bytes.decode('utf-8')

def rsa_encrypt(plaintext: str, encoding='utf-8') -> str:
    """
    使用 RSA 公钥加密数据

    Args:
        plaintext: 明文数据
        public_key_pem: PEM 格式的公钥字符串
        encoding: 编码方式，默认 utf-8

    Returns:
        加密并 Base64 编码后的字符串
    """
    # 加载公钥
    public_key = serialization.load_pem_public_key(
        RSA_PUBLIC_KEY.encode(encoding),
        backend=default_backend()
    )

    # 转换明文为字节
    plaintext_bytes = plaintext.encode(encoding)

    # 加密
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 转换为 Base64 字符串
    return base64.b64encode(ciphertext).decode(encoding)

def rsa_decrypt(ciphertext: str, encoding='utf-8') -> str:
    """
    使用 RSA 私钥解密数据

    Args:
        ciphertext: 加密并 Base64 编码的字符串
        private_key_pem: PEM 格式的私钥字符串
        encoding: 编码方式，默认 utf-8

    Returns:
        解密后的明文
    """
    # 加载私钥
    private_key = serialization.load_pem_private_key(
        RSA_PRIVATE_KEY.encode(encoding),
        password=None,  # 如果私钥有密码，这里需要提供
        backend=default_backend()
    )

    # 转换为字节
    ciphertext_bytes = base64.b64decode(ciphertext)

    # 解密
    plaintext = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext.decode(encoding)