import random
import math
import hashlib

# 生成大素数
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        # 确保数是奇数且大小合适
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p

# 素性测试
def is_prime(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # 将n-1表示为2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # 测试k次
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# 扩展欧几里得算法，计算模逆元
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('模逆元不存在')
    else:
        return x % m

# 生成RSA密钥对
def generate_keypair(bits=1024):
    
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    d = modinv(e, phi)
    
    return ((e, n), (d, n))

# 哈希函数
def hash_message(message):
    # 使用SHA-256哈希消息
    message_bytes = message.encode('utf-8')
    hash_object = hashlib.sha256(message_bytes)
    # 将哈希值转换为整数（取前160位以匹配SHA-1的输出长度）
    return int.from_bytes(hash_object.digest()[:20], 'big')

# 签名消息
def sign_message(private_key, message):
    d, n = private_key
    hashed = hash_message(message)
    signature = pow(hashed, d, n)
    return signature

# 验证签名
def verify_signature(public_key, message, signature):
    e, n = public_key
    hashed = hash_message(message)
    decrypted_signature = pow(signature, e, n)
    return hashed == decrypted_signature

# 测试RSA签名
def test_rsa_signature():
    # 生成密钥对
    print("生成密钥对...")
    public_key, private_key = generate_keypair(1024)
    print(f"公钥: (e={public_key[0]}, n={public_key[1]})")
    print(f"私钥: (d={private_key[0]}, n={private_key[1]})")
    
    # 消息
    message = "Hello, RSA Digital Signature!"

    print(f"\n消息: {message}")
    
    # 签名
    print("\n正在签名...")
    signature = sign_message(private_key, message)
    print(f"签名: {signature}")
    
    # 验证
    print("\n正在验证签名...")
    is_valid = verify_signature(public_key, message, signature)
    print(f"签名验证结果: {'有效' if is_valid else '无效'}")
    
    # 测试篡改消息
    tampered_message = "Hello, RSA Digital Signature?!"
    print("\n测试篡改消息...")
    tampered_is_valid = verify_signature(public_key, tampered_message, signature)
    print(f"篡改后的消息验证结果: {'有效' if tampered_is_valid else '无效'}")

import time
# 性能测试函数
def performance_test():
    key_sizes = [512, 1024, 2048, 3072, 4096]
    num_tests = 5
    message = "Hello, RSA Performance Testing!"
    
    results = {
        'key_size': [],
        'key_gen_time': [],
        'sign_time': [],
        'verify_time': []
    }
    
    for size in key_sizes:
        print(f"\n测试密钥长度: {size} bits")
        key_gen_times = []
        sign_times = []
        verify_times = []
        
        for _ in range(num_tests):
            # 测试密钥生成时间
            start_time = time.time()
            public_key, private_key = generate_keypair(size)
            key_gen_time = time.time() - start_time
            key_gen_times.append(key_gen_time)
            
            # 测试签名时间
            start_time = time.time()
            signature = sign_message(private_key, message)
            sign_time = time.time() - start_time
            sign_times.append(sign_time)
            
            # 测试验证时间
            start_time = time.time()
            is_valid = verify_signature(public_key, message, signature)
            verify_time = time.time() - start_time
            verify_times.append(verify_time)
        
        # 计算平均值
        avg_key_gen = sum(key_gen_times) / num_tests
        avg_sign = sum(sign_times) / num_tests
        avg_verify = sum(verify_times) / num_tests
        
        # 存储结果
        results['key_size'].append(size)
        results['key_gen_time'].append(avg_key_gen)
        results['sign_time'].append(avg_sign)
        results['verify_time'].append(avg_verify)
        
        print(f"平均密钥生成时间: {avg_key_gen:.6f} 秒")
        print(f"平均签名时间: {avg_sign:.6f} 秒")
        print(f"平均验证时间: {avg_verify:.6f} 秒")

if __name__ == "__main__":
    test_rsa_signature()