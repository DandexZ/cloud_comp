#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <cmath>
#include <map>
#include <algorithm>

using namespace std;

// 辅助函数：计算GCD
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// 加密函数
string vigenere_encrypt(const string &plaintext, const string &key) {
    string ciphertext;
    int key_len = key.length();
    
    for (size_t i = 0; i < plaintext.size(); ++i) {
        if (isalpha(plaintext[i])) {
            char base = isupper(plaintext[i]) ? 'A' : 'a';
            char key_char = key[i % key_len];
            char key_base = isupper(key_char) ? 'A' : 'a';
            
            int plain_num = plaintext[i] - base;
            int key_num = key_char - key_base;
            
            char cipher_char = (plain_num + key_num) % 26 + base;
            ciphertext += cipher_char;
        } else {
            ciphertext += plaintext[i];
        }
    }
    
    return ciphertext;
}

// 解密函数
string vigenere_decrypt(const string &ciphertext, const string &key) {
    string plaintext;
    int key_len = key.length();
    
    for (size_t i = 0; i < ciphertext.size(); ++i) {
        if (isalpha(ciphertext[i])) {
            char base = isupper(ciphertext[i]) ? 'A' : 'a';
            char key_char = key[i % key_len];
            char key_base = isupper(key_char) ? 'A' : 'a';
            
            int cipher_num = ciphertext[i] - base;
            int key_num = key_char - key_base;
            
            char plain_char = (cipher_num - key_num + 26) % 26 + base;
            plaintext += plain_char;
        } else {
            plaintext += ciphertext[i];
        }
    }
    
    return plaintext;
}

// 计算字母频率
vector<double> calculate_frequency(const string &text) {
    vector<double> freq(26, 0.0);
    int alpha_count = 0;
    
    for (char c : text) {
        if (isalpha(c)) {
            char lower_c = tolower(c);
            freq[lower_c - 'a']++;
            alpha_count++;
        }
    }
    
    if (alpha_count > 0) {
        for (int i = 0; i < 26; ++i) {
            freq[i] /= alpha_count;
        }
    }
    
    return freq;
}

// Friedman测试计算密钥长度
double friedman_test(const string &ciphertext) {
    vector<double> freq = calculate_frequency(ciphertext);
    double sum = 0.0;
    for (double f : freq) {
        sum += f * f;
    }
    double kp = 0.0667;
    double kr = 1.0 / 26.0;
    double numerator = kp - kr;
    double denominator = sum - kr;
    if (denominator == 0) return 0;
    return numerator / denominator;
}

// Kasiski测试计算密钥长度
int kasiski_test(const string &ciphertext) {
    map<string, vector<int>> sequences;
    for (int len = 3; len <= 5; ++len) {
        for (int i = 0; i <= ciphertext.size() - len; ++i) {
            string seq = ciphertext.substr(i, len);
            bool valid = true;
            for (char c : seq) {
                if (!isalpha(c)) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                sequences[seq].push_back(i);
            }
        }
    }
    vector<int> distances;
    for (const auto &entry : sequences) {
        const vector<int> &positions = entry.second;
        if (positions.size() > 1) {
            for (size_t i = 1; i < positions.size(); ++i) {
                distances.push_back(positions[i] - positions[i-1]);
            }
        }
    }
    if (distances.empty()) return 0;
    int current_gcd = distances[0];
    for (size_t i = 1; i < distances.size(); ++i) {
        current_gcd = gcd(current_gcd, distances[i]);
    }
    return current_gcd;
}

int main() {
    cout << "维吉尼亚密码工具" << endl;
    cout << "1. 加密" << endl;
    cout << "2. 解密" << endl;
    cout << "3. 破解(分析密钥长度)" << endl;
    cout << "4. 退出" << endl;
    
    while(1){
        cout<<endl<<"选择操作: ";
        int choice;
        cin>>choice;
        cin.ignore(); // 清除换行符
        cout<<endl;
        if (choice == 1) {
            string plaintext, key;
            cout << "输入明文: ";
            getline(cin, plaintext);
            cout << "输入密钥: ";
            getline(cin, key);
            
            string ciphertext = vigenere_encrypt(plaintext, key);
            cout << "密文: " << ciphertext << endl;
        } 
        else if (choice == 2) {
            string ciphertext, key;
            cout << "输入密文: ";
            getline(cin, ciphertext);
            cout << "输入密钥: ";
            getline(cin, key);
            
            string plaintext = vigenere_decrypt(ciphertext, key);
            cout << "明文: " << plaintext << endl;
        } 
        else if (choice == 3) {
            string ciphertext;
            cout << "输入密文: ";
            getline(cin, ciphertext);
            
            // Kasiski测试
            int kasiski_length = kasiski_test(ciphertext);
            cout << "Kasiski测试估计的密钥长度: " << kasiski_length << endl;
            
            // Friedman测试
            double friedman_length = friedman_test(ciphertext);
            cout << "Friedman测试估计的密钥长度: " << friedman_length << endl;
            cout << "建议密钥长度: " << round(friedman_length) << endl;
        } 
        else if (choice == 4){
            break;
        }
        else {
            cout << "无效选择" << endl;
        }
    }
    return 0;
}