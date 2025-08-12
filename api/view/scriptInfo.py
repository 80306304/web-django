import json
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Script
from api.selfUtils import rsa_decrypt, result
from django.core.exceptions import ObjectDoesNotExist


# 获取全部脚本列表（GET请求）
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class ScriptListView(APIView):
    """获取所有脚本列表（GET请求）"""

    def get(self, request):
        try:
            # 支持过滤参数
            script_type = request.query_params.get('script_type')
            status_filter = request.query_params.get('status')

            scripts = Script.objects.all()

            # 应用过滤条件
            if script_type:
                scripts = scripts.filter(script_type=script_type)
            if status_filter:
                scripts = scripts.filter(status=status_filter)

            # 转换为字典列表
            data = [model_to_dict(script) for script in scripts]
            return result.success(data, "获取脚本列表成功")

        except Exception as e:
            return result.fail(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 创建脚本（POST请求，带加密处理）
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ScriptCreateView(TokenObtainPairView):
    """创建新脚本（POST请求，加密数据）"""

    def post(self, request, *args, **kwargs):
        # 1. 获取并解密数据
        encrypted_data = request.data.get('data')
        if not encrypted_data:
            return result.fail('缺少加密数据', code=status.HTTP_400_BAD_REQUEST)

        try:
            decrypted_data = json.loads(rsa_decrypt(encrypted_data))
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        # 2. 验证必要字段（ID由系统自动生成）
        required_fields = ['title', 'description', 'script_type', 'required_points']
        for field in required_fields:
            if field not in decrypted_data:
                return result.fail(f"缺少必要字段: {field}", code=status.HTTP_400_BAD_REQUEST)

        # 3. 验证数值字段
        try:
            if int(decrypted_data.get('required_points', 0)) < 0:
                return result.fail("所需点数不能为负数", code=status.HTTP_400_BAD_REQUEST)

            usage_count = decrypted_data.get('usage_count', 0)
            if int(usage_count) < 0:
                return result.fail("使用次数不能为负数", code=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return result.fail("数值字段必须为整数", code=status.HTTP_400_BAD_REQUEST)

        # 4. 验证脚本类型
        valid_types = [choice[0] for choice in Script.SCRIPT_TYPE_CHOICES]
        if decrypted_data['script_type'] not in valid_types:
            return result.fail(f"无效的脚本类型，允许的值: {valid_types}", code=status.HTTP_400_BAD_REQUEST)

        # 5. 创建脚本（状态固定为pending，ID自增）
        try:
            script = Script.objects.create(
                title=decrypted_data['title'],
                description=decrypted_data['description'],
                script_type=decrypted_data['script_type'],
                required_points=int(decrypted_data['required_points']),
                usage_count=int(usage_count),
                status='pending'  # 新创建的脚本状态默认为pending
            )

            return result.success(model_to_dict(script), "脚本创建成功")
        except Exception as e:
            return result.fail(f"创建脚本失败: {str(e)}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 更新脚本（POST请求，ID从加密数据中获取）
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ScriptUpdateView(TokenObtainPairView):
    """更新脚本（POST请求，ID从加密数据中获取）"""

    def post(self, request, *args, **kwargs):
        # 1. 获取并解密数据
        encrypted_data = request.data.get('data')
        if not encrypted_data:
            return result.fail('缺少加密数据', code=status.HTTP_400_BAD_REQUEST)

        try:
            decrypted_data = json.loads(rsa_decrypt(encrypted_data))
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        # 2. 从加密数据中获取脚本ID并验证
        if 'id' not in decrypted_data:
            return result.fail("加密数据中缺少脚本ID", code=status.HTTP_400_BAD_REQUEST)

        try:
            script_id = int(decrypted_data['id'])
        except ValueError:
            return result.fail("脚本ID必须为整数", code=status.HTTP_400_BAD_REQUEST)

        # 3. 查找脚本
        try:
            script = Script.objects.get(id=script_id)
        except ObjectDoesNotExist:
            return result.fail(f"脚本ID {script_id} 不存在", code=status.HTTP_404_NOT_FOUND)

        # 4. 验证数值字段（如果提供）
        try:
            if 'required_points' in decrypted_data and int(decrypted_data['required_points']) < 0:
                return result.fail("所需点数不能为负数", code=status.HTTP_400_BAD_REQUEST)

            if 'usage_count' in decrypted_data and int(decrypted_data['usage_count']) < 0:
                return result.fail("使用次数不能为负数", code=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return result.fail("数值字段必须为整数", code=status.HTTP_400_BAD_REQUEST)

        # 5. 验证脚本类型和状态（如果提供）
        if 'script_type' in decrypted_data:
            valid_types = [choice[0] for choice in Script.SCRIPT_TYPE_CHOICES]
            if decrypted_data['script_type'] not in valid_types:
                return result.fail(f"无效的脚本类型，允许的值: {valid_types}", code=status.HTTP_400_BAD_REQUEST)

        if 'status' in decrypted_data:
            valid_statuses = [choice[0] for choice in Script.STATUS_CHOICES]
            if decrypted_data['status'] not in valid_statuses:
                return result.fail(f"无效的状态，允许的值: {valid_statuses}", code=status.HTTP_400_BAD_REQUEST)

        # 6. 更新脚本信息
        try:
            if 'title' in decrypted_data:
                script.title = decrypted_data['title']
            if 'description' in decrypted_data:
                script.description = decrypted_data['description']
            if 'script_type' in decrypted_data:
                script.script_type = decrypted_data['script_type']
            if 'required_points' in decrypted_data:
                script.required_points = int(decrypted_data['required_points'])
            if 'usage_count' in decrypted_data:
                script.usage_count = int(decrypted_data['usage_count'])
            if 'status' in decrypted_data:
                script.status = decrypted_data['status']

            script.save()

            return result.success(model_to_dict(script), "脚本更新成功")
        except Exception as e:
            return result.fail(f"更新脚本失败: {str(e)}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 删除脚本（逻辑删除，ID从加密数据中获取）
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ScriptDeleteView(TokenObtainPairView):
    """删除脚本（逻辑删除，ID从加密数据中获取）"""

    def post(self, request, *args, **kwargs):
        # 1. 获取并解密数据
        encrypted_data = request.data.get('data')
        if not encrypted_data:
            return result.fail('缺少加密数据', code=status.HTTP_400_BAD_REQUEST)

        try:
            decrypted_data = json.loads(rsa_decrypt(encrypted_data))
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        # 2. 从加密数据中获取脚本ID并验证
        if 'id' not in decrypted_data:
            return result.fail("加密数据中缺少脚本ID", code=status.HTTP_400_BAD_REQUEST)

        try:
            script_id = int(decrypted_data['id'])
        except ValueError:
            return result.fail("脚本ID必须为整数", code=status.HTTP_400_BAD_REQUEST)

        # 3. 查找脚本并修改状态为banned
        try:
            script = Script.objects.get(id=script_id)
            # 逻辑删除：将状态改为banned
            script.status = 'banned'
            script.save()
            return result.success(model_to_dict(script), "脚本已禁用（逻辑删除）")
        except ObjectDoesNotExist:
            return result.fail(f"脚本ID {script_id} 不存在", code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return result.fail(f"操作失败: {str(e)}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
