import random
import time
import requests
from api.function.sendPush import sendMsg


def get_ad(token,uuid,pushToken:str=None):
    if pushToken:
        sendMsg(pushToken, "任务开始通知", "广告任务已开始")
    while True:
        time.sleep(1)
        url = f"https://game.xywzzj.com/gm1/kind11/xiadan?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"kid":"actBox","hdcid":"1","dc":"1"}

        res = requests.post(url, headers=headers, json=data)
        order11Id = res.json().get("order11Id")
        print(res.json())
        url= f"https://game.xywzzj.com/gm1/kind11/success?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        data = {"order11Id":order11Id}
        res = requests.post(url, headers=headers, json=data).json()
        print(res.get("win").get("msg")!="请勿重复点击")
        if res.get("type") == 0 and res.get("win").get("msg")!="请勿重复点击":
            print("广告已看完")
            if pushToken:
                sendMsg(pushToken, "任务完成通知","广告任务已完成")
            return f"{token}任务已完成"
            break;
        else:
            print("正在看广告")

def finish_game(token,uuid,pushToken:str=None):
    count = 0
    steps = [
        "处理装备战力对比与替换",
        "挑战BOSS 1",
        "挑战BOSS 2",
        "挑战BOSS 3",
        "挑战BOSS 4",
        "道童更换操作",
        "万象演算流程",
        "任务奖励查询",
        "钓鱼操作",
        "斗法"
    ]
    total_steps = len(steps)
    for i in range(3000):
        try:
            time.sleep(1)
            count += 1
            # 循环次数提示
            print(f"正在运行第 {count} 次循环")
            # 1. 处理装备替换
            print(f"步骤 1/{total_steps}：{steps[0]}")
            if "actEquip字段缺失" in stove(token,uuid):
                print("账户已在别处登录,已结束程序")
                break

            # 2-5. 挑战BOSS
            for i in range(4):
                boss_num = i + 1
                print(f"步骤 {i + 2}/{total_steps}：{steps[i + 1]}")
                fight_boss(token, boss_num,uuid)

            # 6. 道童更换
            print(f"步骤 6/{total_steps}：{steps[5]}")
            steal(token,uuid)

            # 7. 万象演算
            print(f"步骤 7/{total_steps}：{steps[6]}")
            yansuan(token,uuid)

            # 8. 任务奖励
            print(f"步骤 8/{total_steps}：{steps[7]}")
            rwd(token,uuid)

            # 9. 钓鱼
            print(f"步骤 9/{total_steps}：{steps[8]}")
            fish(token,uuid)

            # 10. 斗法
            print(f"步骤 10/{total_steps}：{steps[9]}")
            get5(token,uuid)

            # 循环结束提示
            print(f"第 {count} 次循环执行完毕\n")
        except Exception as e:
            print(f"❌ 运行过程中出现问题：{str(e)}")
        if pushToken:
            sendMsg(pushToken, "任务完成通知", "广告任务已完成")
        return "所有任务已完成"

def stove(token,uuid):
    """
    处理装备开箱、战力对比及替换决策的完整流程
    （新装备战力更高时会自动替换，反之则保留原有装备）
    :param token: 访问令牌
    :return: 操作结果信息
    """
    try:
        # 1. 获取战力信息并比较
        get_url = f"https://game.hzp4687.com/gm1/equip/openBox95?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        get_headers = {"Content-Type": "application/json"}
        get_data = {"needNum": 1}

        # 发送获取请求并处理可能的网络错误
        try:
            response = requests.post(get_url, headers=get_headers, json=get_data, timeout=10)
            response.raise_for_status()  # 检查HTTP请求状态码
        except requests.exceptions.RequestException as e:
            return f"❌ 获取装备战力信息失败：网络连接出现问题 - {str(e)}"

        # 解析JSON响应
        try:
            res = response.json()
        except ValueError:
            return "❌ 获取装备战力信息失败：收到的响应格式不正确"

        # 安全获取嵌套字典数据
        try:
            act_equip = res.get("actEquip")
            if not act_equip:
                return "❌ 获取装备战力信息失败：未找到装备数据（actEquip字段缺失）"

            u_data = act_equip.get("u")
            if not u_data:
                return "❌ 获取装备战力信息失败：未找到详细数据（u字段缺失）"

            linshi_old = u_data.get("linshiOld")  # 原有装备信息
            linshi_95 = u_data.get("linshi95")    # 新开出的装备信息
            if not linshi_old or not linshi_95:
                return "❌ 获取装备战力信息失败：缺少新旧装备的战力数据（linshiOld或linshi95字段缺失）"

            old_eps = linshi_old.get("eps", {})  # 旧装备战力详情
            new_eps = linshi_95.get("1", {}).get("eps", {})  # 新装备战力详情
        except AttributeError as e:
            return f"❌ 解析装备战力信息失败：数据格式有误 - {str(e)}"

        # 计算战力总和并打印对比
        old_total = sum(old_eps.values()) if isinstance(old_eps, dict) else 0
        new_total = sum(new_eps.values()) if isinstance(new_eps, dict) else 0
        print(f"📊 战力对比：旧装备总战力 {old_total} vs 新装备总战力 {new_total}")

        # 2. 根据比较结果执行替换或保留操作
        if old_total > new_total:
            # 旧装备更强，执行保留操作
            sell_url = f"https://game.xywzzj.com/gm1/equip/deal95?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
            sell_data = {"xbid": "1"}

            try:
                sell_response = requests.post(sell_url, headers=get_headers, json=sell_data, timeout=10)
                sell_response.raise_for_status()
                print(f"❌ 旧装备战力更高（{old_total} > {new_total}），不进行替换")
                return f"❌ 操作成功：旧装备战力更优（{old_total} > {new_total}），已保留原有装备"
            except requests.exceptions.RequestException as e:
                return f"❌ 保留装备失败：网络连接出现问题 - {str(e)}"

        else:
            # 新装备更强，执行替换操作
            buy_url = f"https://game.xywzzj.com/gm1/equip/tihuan?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
            buy_data = {"type": 1, "xbid": "1"}

            try:
                buy_response = requests.post(buy_url, headers=get_headers, json=buy_data, timeout=10)
                buy_response.raise_for_status()
                print(f"✅ 新装备战力更高（{new_total} ≥ {old_total}），已完成替换")
                sendMsg("b849d1083968467fa9e7363a51d1e076","抽到新装备",f"✅ 新装备战力更高（{new_total} ≥ {old_total}），已完成替换")
                return f"✅ 操作成功：新装备战力更优（{new_total} ≥ {old_total}），已替换原有装备"
            except requests.exceptions.RequestException as e:
                return f"❌ 替换装备失败：网络连接出现问题 - {str(e)}"

    except Exception as e:
        return f"❌ 操作失败：发生未知错误 - {str(e)}"

def rwd(token,uuid):
    """
    查询任务完成状态及奖励领取情况的完整流程
    （检查任务是否完成，返回清晰的状态说明）
    :param token: 访问令牌
    :return: 任务状态信息（字符串）
    """
    # 配置参数集中管理，便于维护
    config = {
        "base_url": "https://game.xywzzj.com",
        "path": "gm1/task/rwd",
        "uuid": f"{uuid}",
        "version": "1.0.0",
        "headers": {"Content-Type": "application/json"}
    }

    try:
        # 构建查询任务状态的请求URL
        timestamp = time.time()
        url = f"{config['base_url']}/{config['path']}?uuid={config['uuid']}&token={token}&version={config['version']}&time={timestamp}"

        # 发送任务状态查询请求（添加超时控制，避免无限等待）
        try:
            response = requests.post(
                url,
                headers=config["headers"],
                json={},
                timeout=10  # 10秒超时
            )
            response.raise_for_status()  # 检查HTTP错误状态码（4xx/5xx）
        except requests.exceptions.RequestException as e:
            return f"任务状态查询失败：网络连接出现问题 - {str(e)}"

        # 获取响应内容
        response_text = response.text

        # 尝试解析JSON（即使解析失败也不影响后续状态判断）
        try:
            response_json = response.json()
        except ValueError:
            print("温馨提示：接口返回的内容不是标准JSON格式，不影响状态判断哦~")

        # 判断并描述任务状态
        if '任务未完成' in response_text:
            result = "❌ 任务状态：当前任务尚未完成，暂时无法领取奖励"
        else:
            result = "✅ 任务状态：任务已顺利完成，可以领取奖励啦"

        print(result)
        return result

    except Exception as e:
        # 捕获所有未预料的异常
        error_msg = f"任务奖励查询过程中发生未知错误：{str(e)}"
        print(error_msg)
        return error_msg

def steal(token,uuid):
    """
    道童更换操作流程：检查附近洞天空位，自动筛选可用位置并尝试更换道童
    （若找到双方均未占用的空位，会尝试更换；无空位或道童不足时返回对应状态）
    :param token: 访问令牌
    :return: 操作结果信息（字符串）
    """
    try:
        # 1. 查询附近洞天信息，寻找可用空位
        query_url = f"https://game.xywzzj.com/gm1/dongtian/nears?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
        query_headers = {"Content-Type": "application/json"}

        try:
            # 发送附近洞天查询请求
            query_res = requests.post(query_url, headers=query_headers, json={}, timeout=10)
            query_res.raise_for_status()
            nearby_data = query_res.json()
        except requests.exceptions.RequestException as e:
            return f"查询附近洞天信息失败：网络连接不太顺畅呢 - {str(e)}"
        except ValueError:
            return "查询附近洞天信息失败：返回的数据格式不太对哦"

        # 提取附近洞天列表（nearsActDongTian为附近的洞天活动数据）
        nearby_dongtian = nearby_data.get("nearsActDongTian", {})
        available_ids = list(nearby_dongtian.keys())  # 可用的洞天标识列表

        target_uuid = ""  # 目标洞天标识
        target_pos = ""  # 目标空位位置（pos为位置标识）

        if available_ids:
            # 随机选一个洞天，检查是否有双方均未占用的空位
            selected_id = random.choice(available_ids)
            dongtian_details = nearby_dongtian[selected_id].get("dongtian", {})  # 该洞天的详细位置信息

            max_pos = -1
            best_pos_key = ""
            for pos_key, pos_info in dongtian_details.items():
                # 筛选"my.user"和"he.user"均为null（未占用）的位置
                my_occupy = pos_info.get("my", {}).get("user")  # 我方是否占用
                he_occupy = pos_info.get("he", {}).get("user")  # 对方是否占用
                if my_occupy is None and he_occupy is None:
                    current_pos = int(pos_info.get("pos", -1))
                    if current_pos > max_pos:
                        max_pos = current_pos
                        best_pos_key = pos_key  # 记录最优空位（pos最大的）

            target_uuid = selected_id
            if best_pos_key:
                print(f"✅ 找到可用空位！选中的洞天标识：{target_uuid}，空位位置：{best_pos_key}")
                target_pos = best_pos_key
            else:
                print(f"❌ 当前选中的洞天（{selected_id}）中，没有双方均未占用的空位哦")
        else:
            print("❌ 暂时没有查询到任何可用的洞天呢")

        # 2. 若找到空位，尝试更换道童
        if target_pos:
            change_url = f"https://game.hzp4687.com/gm1/dongtian/lache?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
            change_data = {"fuuid": target_uuid, "pos": target_pos, "knum": 2}

            try:
                change_res = requests.post(change_url, headers=query_headers, json=change_data, timeout=10)
                change_res.raise_for_status()
                result = change_res.json()
            except requests.exceptions.RequestException as e:
                return f"更换道童时出了点小问题：网络不太稳定呢 - {str(e)}"
            except ValueError:
                return "更换道童失败：返回的结果格式不太对哦"

            # 判断道童更换结果
            if result.get("type") == 1:
                message = "✅ 道童更换成功啦！已为你换上新道童~"
            else:
                message = "❌ 道童更换失败：目前可用的道童不足呢，请稍后再试"
            print(message)
            return message
        else:
            # 无可用空位时的结果
            return "操作结束：没有找到合适的空位，暂时无法更换道童哦"

    except Exception as e:
        error_msg = f"道童更换过程中出现意外：{str(e)}"
        print(error_msg)
        return error_msg

def hdHlChou(token,uuid):
    url = f"https://game.hzp4687.com/gm1/huodong/hdHlChou?uuid={uuid}&token={token}&version=1.0.0&time={time.time()} "
    headers = {
        "Content-Type": "application/json",
    }
    data = {"hdcid":"2","num":1}
    res = requests.post(url, headers=headers, json=data).json()
    print(res)
#斗法
def get5(token,uuid):
    """
      竞技场挑战最低等级对手的完整流程
      功能：获取5个对手→筛选等级最低的→发起战斗→处理战斗结果（含错误信息）
      :param token: 访问令牌
      :return: 操作结果描述（字符串）
      """
    # 基础配置参数
    base_url = "https://game.xywzzj.com"
    common_params = f"uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
    headers = {"Content-Type": "application/json"}

    try:
        # 1. 获取5个对手信息
        get5_url = f"{base_url}/gm1/jjc/get5?{common_params}"
        try:
            # 发送请求并设置超时
            get5_response = requests.post(
                get5_url,
                headers=headers,
                json={},
                timeout=10  # 10秒超时控制
            )
            get5_response.raise_for_status()  # 检查HTTP状态码（4xx/5xx会抛异常）
        except requests.exceptions.RequestException as e:
            return f"❌ 获取对手列表失败（网络错误）：{str(e)}"

        # 解析对手列表JSON
        try:
            get5_data = get5_response.json()
        except ValueError:
            return "❌ 获取对手列表失败：响应不是有效的JSON格式"

        # 提取并校验对手数据结构
        try:
            act_jjc_info = get5_data.get("actJjcInfo", {})
            opponent_list = act_jjc_info.get("get5", [])

            # 检查对手列表是否为有效列表
            if not isinstance(opponent_list, list):
                return "❌ 获取对手列表失败：数据格式错误（非列表）"
            # 检查列表是否为空
            if len(opponent_list) == 0:
                return "❌ 获取对手列表失败：未返回任何对手"
        except AttributeError as e:
            return f"❌ 对手数据解析失败（结构错误）：{str(e)}"

        # 2. 筛选等级最低的对手
        min_level = 999
        target_uuid = ""
        try:
            for opponent in opponent_list:
                # 跳过非字典格式的无效数据
                if not isinstance(opponent, dict):
                    continue

                # 提取等级和UUID（跳过缺失关键信息的对手）
                opponent_level_str = opponent.get("level")
                opponent_uuid = opponent.get("uuid")
                if not opponent_level_str or not opponent_uuid:
                    continue

                # 转换等级为整数（处理非数字格式的情况）
                try:
                    opponent_level = int(opponent_level_str)
                except ValueError:
                    continue  # 跳过等级格式错误的对手

                # 更新最低等级对手
                if opponent_level < min_level:
                    min_level = opponent_level
                    target_uuid = opponent_uuid

            # 检查是否找到有效对手
            if not target_uuid:
                return "❌ 未找到有效对手：所有对手数据不完整"

            print(f"✅ 筛选到最低等级对手 - UUID: {target_uuid}, 等级: {min_level}")
        except Exception as e:
            return f"❌ 筛选对手时出错：{str(e)}"

        # 3. 向最低等级对手发起战斗
        fight_url = f"{base_url}/gm1/jjc/fight?{common_params}"
        fight_data = {"fuuid": target_uuid}
        try:
            fight_response = requests.post(
                fight_url,
                headers=headers,
                json=fight_data,
                timeout=10
            )
            fight_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"❌ 战斗请求失败（网络错误）：{str(e)}"

        # 解析战斗响应（处理type=0的错误信息）
        try:
            fight_result = fight_response.json()
            fight_type = fight_result.get("type")

            # 处理type=0的错误场景（如门票不足）
            if fight_type == 0:
                win_info = fight_result.get("win", {})
                error_msg = win_info.get("msg", "未知错误")
                # 兼容msg为列表或字符串的格式
                if isinstance(error_msg, list):
                    error_msg = "; ".join(error_msg)
                print(f"❌ 战斗失败：{error_msg}")
                return f"❌ 战斗失败：{error_msg}"
            else:
                print(f"✅ 战斗发起成功：已向 UUID={target_uuid}（等级{min_level}）发起挑战")
                sendMsg("b849d1083968467fa9e7363a51d1e076", "斗法成功",
                        f"✅ 斗法成功")
                return f"✅ 战斗发起成功：挑战等级{min_level}的对手（UUID={target_uuid}）"
        except ValueError:
            return "❌ 战斗响应解析失败：不是有效的JSON格式"
        except Exception as e:
            return f"❌ 处理战斗结果时出错：{str(e)}"

    # 捕获所有未预料的异常
    except Exception as e:
        error_detail = f"竞技场操作发生未知错误：{str(e)}"
        print(f"❌ {error_detail}")
        return error_detail

# 看广告
def get_ad(token,uuid):
    url = f"https://game.xywzzj.com/gm1/kind11/xiadan?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
    headers = {
        "Content-Type": "application/json",
    }
    data = {"kid":"actBox","hdcid":"1","dc":"1"}
    # data = {"kid": "actFuShi", "hdcid": "1", "dc": "1"}
    res = requests.post(url, headers=headers, json=data)
    order11Id = res.json().get("order11Id")
    print(order11Id)
    time.sleep(1)
    url= f"https://game.xywzzj.com/gm1/kind11/success?uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
    data = {"order11Id":order11Id}
    res = requests.post(url, headers=headers, json=data)
    print(res.json())

#万象命盘
def yansuan(token,uuid):
    """
    处理万象演算的完整流程：获取装备战力数据、对比新旧战力，并自动决定是否更换装备
    （新装备战力更高时将更换，反之则保留当前装备）
    :param token: 访问令牌
    :return: 操作结果信息（字符串）
    """
    # 基础配置集中管理
    base_url = "https://game.xywzzj.com"
    common_params = f"uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"
    headers = {"Content-Type": "application/json"}

    try:
        # 1. 执行演算请求，获取新旧装备战力数据
        yansuan_url = f"{base_url}/gm1/wanxiang/yansuan?{common_params}"
        yansuan_data = {"isOpen": 0}

        try:
            # 发送演算请求（添加超时控制）
            yansuan_res = requests.post(
                yansuan_url,
                headers=headers,
                json=yansuan_data,
                timeout=10
            )
            yansuan_res.raise_for_status()  # 检查HTTP错误状态码
        except requests.exceptions.RequestException as e:
            return f"演算请求失败：网络连接出现问题 - {str(e)}"

        # 解析演算响应JSON
        try:
            res = yansuan_res.json()
        except ValueError:
            return "演算请求失败：收到的响应格式不正确"

        # 安全提取嵌套数据（防止KeyError和AttributeError）
        try:
            act_wanxiang = res.get("actWanXiang", {})
            if not act_wanxiang:
                return "演算数据解析失败：缺少装备演算主数据（actWanXiang字段）"

            # 获取新演算的装备数据
            new_data = act_wanxiang.get("linshi", {})  # 临时演算的新装备数据
            new_id = new_data.get("id")
            new_eps = new_data.get("eps", {})  # 新装备战力详情

            # 获取当前装备数据（用于对比）
            mp_list = act_wanxiang.get("mpList", {})  # 当前装备列表
            old_data = mp_list.get(new_id, {}) if new_id is not None else {}  # 对应位置的旧装备
            old_eps = old_data.get("eps", {})  # 旧装备战力详情
        except AttributeError as e:
            return f"演算数据结构错误：数据格式不符合预期 - {str(e)}"

        # 计算新旧战力值（处理可能的空字典和类型转换问题）
        try:
            # 提取并转换新装备第一个战力值
            new_hp = int(next(iter(new_eps.values()))) if new_eps else 0
            # 提取并转换当前装备第一个战力值
            old_hp = int(next(iter(old_eps.values()))) if old_eps else 0
        except (StopIteration, ValueError) as e:
            return f"战力计算失败：战力数据格式错误 - {str(e)}"

        print(f"当前装备战力: {old_hp}，新演算装备战力：{new_hp}")

        # 2. 根据战力比较结果执行对应操作
        if old_hp < new_hp:
            # 新装备战力更高，执行更换操作
            buy_url = f"{base_url}/gm1/wanxiang/zhuangbei?{common_params}"
            try:
                buy_res = requests.post(buy_url, headers=headers, json={}, timeout=10)
                buy_res.raise_for_status()
                print("新装备战力更高，已完成更换")
                return "✅ 操作成功：新装备战力更优，已更换为新装备"
            except requests.exceptions.RequestException as e:
                return f"更换装备失败：网络连接出现问题 - {str(e)}"
        else:
            # 当前装备战力更高，执行保留操作
            sell_url = f"{base_url}/gm1/wanxiang/yiwang?{common_params}"
            try:
                sell_res = requests.post(sell_url, headers=headers, json={}, timeout=10)
                sell_res.raise_for_status()
                print("当前装备战力更高，不进行更换")
                return "❌ 操作成功：当前装备战力更优，保持原有装备"
            except requests.exceptions.RequestException as e:
                return f"保留装备失败：网络连接出现问题 - {str(e)}"

    except Exception as e:
        # 捕获所有未预料的异常
        error_msg = f"万象演算流程发生未知错误：{str(e)}"
        print(error_msg)
        return error_msg

def fish(token,uuid):
    """
    执行钓鱼操作的完整流程：包含抽鱼（获取渔获）和结果处理步骤，最终返回钓鱼成败信息
    :param token: 访问令牌
    :return: 操作结果信息（字符串）
    """
    # 基础配置集中管理
    base_url = "https://game.xywzzj.com"
    headers = {"Content-Type": "application/json"}
    common_params = f"uuid={uuid}&token={token}&version=1.0.0&time={time.time()}"

    try:
        # 1. 执行抽鱼操作（获取渔获）
        chou_url = f"{base_url}/gm1/fushi/chou?{common_params}"  # 抽鱼请求地址
        try:
            # 发送抽鱼请求（添加超时控制）
            chou_res = requests.post(chou_url, headers=headers, json={}, timeout=10)
            chou_res.raise_for_status()  # 检查HTTP错误状态码
        except requests.exceptions.RequestException as e:
            return f"抽鱼操作失败：网络连接或请求出现问题 - {str(e)}"

        # 2. 执行渔获处理操作（出售/确认结果）
        chushou_url = f"{base_url}/gm1/fushi/chushou?{common_params}"  # 渔获处理请求地址
        chushou_data = {"type": 0}
        try:
            # 发送渔获处理请求
            chushou_res = requests.post(chushou_url, headers=headers, json=chushou_data, timeout=10)
            chushou_res.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"渔获处理失败：网络连接或请求出现问题 - {str(e)}"

        # 3. 解析处理结果
        try:
            res_json = chushou_res.json()  # 解析响应数据
        except ValueError:
            return "解析钓鱼结果失败：收到的响应格式不正确（非有效JSON）"

        # 安全判断钓鱼结果
        result_type = res_json.get("type")
        if result_type == 0:
            message = "❌ 钓鱼失败：未成功获取渔获"
        else:
            message = "✅ 钓鱼成功：已顺利获取渔获并完成处理"

        print(message)
        return message  # 确保返回结果信息

    except Exception as e:
        # 捕获未预料的异常
        error_msg = f"钓鱼操作发生未知错误：{str(e)}"
        print(error_msg)
        return error_msg


    except Exception as e:
        # 捕获其他未知异常
        error_msg = f"钓鱼操作发生未知错误：{str(e)}"
        print(error_msg)
        return error_msg

def fight_boss(token, combat_type,uuid):
    """
    通用战斗处理函数，用于处理不同类型的游戏战斗请求

    该函数根据指定的战斗类型，向对应的游戏服务器发送单步或多步请求，
    处理战斗流程并返回包含各步骤执行情况及最终结果的信息。

    参数:
        token (str): 访问游戏服务器的授权令牌
        combat_type (int): 战斗类型标识，支持以下类型：
            1 - 原BOSS战斗（boss1）
            2 - 原BOSS战斗（boss2）
            3 - 原BOSS战斗（boss3）
            4 - 新增PVE战斗（多步流程）

    返回:
        str: 战斗结果信息字符串，包含各步骤执行状态及最终战斗结果

    示例:
        >>> fight_boss("user_auth_token", 1)
        "boss1第1步请求成功; 挑战boss1成功，✅ 胜利！"
    """
    # 战斗配置映射：包含基础URL和请求路径（支持单步/多步请求）
    combat_configs = {
        1: {
            "base_url": "https://game.xywzzj.com",
            "paths": ["gm1/liudao/fight"],  # 单步请求
            "name": "boss1"
        },
        2: {
            "base_url": "https://game.xywzzj.com",
            "paths": ["gm1/pve/jyFight"],
            "name": "boss2"
        },
        3: {
            "base_url": "https://game.xywzzj.com",
            "paths": ["gm1/pvw/jyFight"],
            "name": "boss3"
        },
        4: {
            "base_url": "https://game.hzp4687.com",
            "paths": ["gm1/pve/fight", "gm1/pve/fightEnd"],  # 多步请求
            "name": "pve战斗",
            "data": [{}, {"ftype": "pve"}],  # 对应步骤的请求数据
            "sleep": 1  # 步骤间等待时间（秒）
        }
    }

    # 验证战斗类型
    if combat_type not in combat_configs:
        return f"😮 错误：战斗类型 {combat_type} 不存在哦，请选择1-4之间的类型~"

    config = combat_configs[combat_type]
    headers = {"Content-Type": "application/json"}
    results = []

    try:
        # 执行多步请求
        for i, path in enumerate(config["paths"]):
            # 构建URL（注意：第2步pve/fightEnd的uuid为空）
            uuid_param = f"{uuid}" if i == 0 or combat_type != 4 else ""
            url = f"{config['base_url']}/{path}?uuid={uuid_param}&token={token}&version=1.0.0&time={time.time()}"

            # 获取当前步骤的请求数据（默认空字典）
            data = config.get("data", [{}])[i] if config.get("data") else {}

            # 发送请求
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            results.append(f"✅ {config['name']}第{i + 1}步请求已完成")

            # 步骤间等待（如果配置了）
            if i < len(config["paths"]) - 1 and config.get("sleep"):
                time.sleep(config["sleep"])

        # 处理最终结果（针对有响应解析需求的战斗类型）
        if combat_type in [1, 2, 3]:
            # 解析最后一步的响应
            try:
                res = response.json()
                if res.get("type") == 1:
                    act_pve = res.get("actPveJyFight", {})
                    end_info = act_pve.get("end", {})
                    win_status = end_info.get("win")
                    result = f"挑战{config['name']}成功，{'✅ 胜利！' if win_status == 1 else '❌ 未获胜'}"
                else:
                    result = f"挑战{config['name']}未能完成"
            except ValueError:
                result = f"挑战{config['name']}时遇到问题：无法解析战斗结果"
            results.append(result)

        # 整合结果
        final_result = "; ".join(results)
        print(final_result)
        return final_result

    except requests.exceptions.RequestException as e:
        error_msg = f"⚠️ {config['name']}请求出现问题：{str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"😮 {config['name']}发生意外：{str(e)}"
        print(error_msg)
        return error_msg