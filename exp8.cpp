#include <iostream>
#include <cmath>
#include <ctime>
#include <vector>
using namespace std;

// 检查是否为素数
bool isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i <= sqrt(n); i++)
        if (n % i == 0) return false;
    return true;
}

// 计算最大公约数
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

// 生成密钥对
void generateKeys(int p, int q, int &n, int &e, int &d) {
    n = p * q;
    int phi = (p-1)*(q-1);
    
    // 选择公钥e (1 < e < phi，且与phi互质)
    for (e = 2; e < phi; e++)
        if (gcd(e, phi) == 1) break;
    
    // 计算私钥d (d*e ≡ 1 mod phi)
    for (d = 2; d < phi; d++)
        if ((d * e) % phi == 1) break;
}

// 加密函数
int encrypt(int msg, int e, int n) {
    int result = 1;
    for (int i = 0; i < e; i++)
        result = (result * msg) % n;
    return result;
}

// 解密函数
int decrypt(int cipher, int d, int n) {
    int result = 1;
    for (int i = 0; i < d; i++)
        result = (result * cipher) % n;
    return result;
}

// 因式分解破解
void factorize(int n, int &p, int &q) {
    clock_t start = clock();
    for (p = 2; p <= sqrt(n); p++) {
        if (n % p == 0 && isPrime(p)) {
            q = n / p;
            if (isPrime(q)) break;
        }
    }
    clock_t end = clock();
    double time = double(end - start) / CLOCKS_PER_SEC;
    cout << "破解耗时: " << time << "秒" << endl;
}

int main() {
    cout << "======== RSA加解密实验 ========" << endl;
    
    // 实验1：完整的RSA流程演示（32位）
    {
        cout << "\n[实验1] 32位RSA完整流程演示" << endl;
        int p = 61, q = 53; // 两个小素数
        int n, e, d;
        
        generateKeys(p, q, n, e, d);
        cout << "公钥(e,n): (" << e << ", " << n << ")" << endl;
        cout << "私钥(d,n): (" << d << ", " << n << ")" << endl;
        
        int msg = 123; // 原始消息
        cout << "原始消息: " << msg << endl;
        
        int cipher = encrypt(msg, e, n);
        cout << "加密结果: " << cipher << endl;
        
        int decrypted = decrypt(cipher, d, n);
        cout << "解密结果: " << decrypted << endl;
    }
    
    // 实验2：不同密钥长度的破解时间比较
    cout << "\n[实验2] 不同密钥长度的破解时间比较" << endl;
    vector<pair<int, string>> testCases = {
        {32, "32位 (4-5位十进制)"},
        {64, "64位 (19-20位十进制)"},
        {128, "128位 (38-39位十进制)"},
        {256, "256位 (77-78位十进制)"},
        {512, "512位 (154-155位十进制)"}
    };
    
    for (auto &test : testCases) {
        cout << "\n测试密钥长度: " << test.second << endl;
        
        // 生成两个素数
        int bits = test.first / 2;
        int min = pow(2, bits-1);
        int max = pow(2, bits) - 1;
        
        int p = 0, q = 0;
        while (!isPrime(p)) p = rand() % (max - min + 1) + min;
        while (!isPrime(q)) q = rand() % (max - min + 1) + min;
        
        int n = p * q;
        cout << "模数n: " << n << endl;
        
        int found_p, found_q;
        factorize(n, found_p, found_q);
        
        if (found_p * found_q == n) {
            cout << "破解成功! 因数: " << found_p << " 和 " << found_q << endl;
        } else {
            cout << "破解失败!" << endl;
        }
    }
    system("pause");
    return 0;
}