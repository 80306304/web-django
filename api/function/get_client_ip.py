def get_client_ip(request):
    """获取客户端真实IP（兼容反向代理）"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For格式：客户端IP, 代理1IP, 代理2IP...，取第一个有效IP
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # 未使用代理时，直接取REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR', 'unknown')

    return ip