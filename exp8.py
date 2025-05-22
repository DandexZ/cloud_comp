import math
import random
import time
from multiprocessing import Process, Queue


def is_prime(n):
    """检查是否为素数"""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    """生成指定范围内的素数"""
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p):
            return p

def gcd(a, b):
    """计算最大公约数"""
    while b != 0:
        a, b = b, a % b
    return a

def modinv(e, phi):
    """计算模逆元"""
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

def generate_keys(p, q):
    """生成RSA密钥对"""
    n = p * q
    phi = (p-1) * (q-1)
    
    # 选择公钥e
    for e in range(2, phi):
        if gcd(e, phi) == 1:
            break
    
    # 计算私钥d
    d = modinv(e, phi)
    
    return (e, n), (d, n)

def encrypt(msg, public_key):
    """加密函数"""
    e, n = public_key
    return pow(msg, e, n)

def decrypt(cipher, private_key):
    """解密函数"""
    d, n = private_key
    return pow(cipher, d, n)

def factorize(n, result_queue):
    """因式分解函数"""
    start_time = time.time()
    
    for p in range(2, int(math.sqrt(n)) + 1):
        if n % p == 0 and is_prime(p):
            q = n // p
            if is_prime(q):
                result_queue.put((p, q, time.time() - start_time))
                return
    
    result_queue.put((None, None, time.time() - start_time))

def crack_rsa(n, timeout=120):
    """破解RSA"""
    print(f"开始破解n={n}...")
    result_queue = Queue()
    p = Process(target=factorize, args=(n, result_queue))
    p.start()
    
    # 等待结果或超时
    p.join(timeout)
    
    if p.is_alive():
        p.terminate()
        p.join()
        return None, None, None, "失败（超过120秒）"
    
    p, q, time_used = result_queue.get()
    if p and q:
        return p, q, time_used, "成功"
    else:
        return None, None, time_used, "失败（未找到因数）"

def main():
    print("======== RSA加解密实验========")
    
    # 实验1：完整的RSA流程演示（8位）
    print("\n[实验1] 8位RSA完整流程")
    p = 23
    q = 29
    public_key, private_key = generate_keys(p, q)
    print(f"公钥(e,n): {public_key}")
    print(f"私钥(d,n): {private_key}")
    
    msg = 42  # 原始消息必须小于n
    print(f"原始消息: {msg}")
    
    cipher = encrypt(msg, public_key)
    print(f"加密结果: {cipher}")
    
    decrypted = decrypt(cipher, private_key)
    print(f"解密结果: {decrypted}")
    
    # 实验2：不同密钥长度的破解时间比较
    print("\n[实验2] 不同密钥长度的破解时间比较（最多等待120秒）")
    test_cases = [
        (16, "16位"),
        (20, "20位"),
        (24, "24位"),
        (26, "26位"),
        (28, "28位"),
        (30, "30位"),
        (32, "32位")
    ]
    
    for bits, description in test_cases:
        print(f"\n测试密钥长度: {description}")
        
        # 生成两个素数
        min_val = 10 ** (bits//4)  # 调整范围使n不会太大
        max_val = 10 ** (bits//4 + 1)
        
        p = generate_prime(min_val, max_val)
        q = generate_prime(min_val, max_val)
        n = p * q
        print(f"模数n: {n} (位数: {len(str(n))})")
        
        # 尝试破解
        found_p, found_q, time_used, status = crack_rsa(n)
        
        if status.startswith("成功"):
            print(f"破解{status}! 因数: {found_p} 和 {found_q}")
        else:
            print(f"破解{status}")
        
        print(f"耗时: {time_used:.2f}秒" if time_used is not None else "超过120秒")

if __name__ == "__main__":
    main()