# PID调参工具

## 安装依赖

### 方法1：使用UV（推荐）
```bash
# 安装uv（如果还没有安装）
pip install uv

# 安装项目依赖
uv sync

# 或者从GitHub/其他源安装
uv pip install -e .
```

### 方法2：使用传统pip
```bash
pip install -r requirements.txt
```

## 运行工具

### 使用UV（推荐）
```bash
# 运行PID调参工具
uv run pid-tuner

# 运行测试接收器
uv run pid-receiver

# 或者直接运行Python文件
uv run python pid_tuner.py
uv run python test_receiver.py
```

### 使用传统方式
```bash
python pid_tuner.py
python test_receiver.py
```

## UV的优势

- 🚀 **极快的安装速度**：比pip快10-100倍
- 🔒 **可靠的依赖管理**：自动解决版本冲突
- 🛠️ **现代化工具链**：统一的项目管理体验
- 📦 **内置虚拟环境**：无需手动管理venv

详细的UV使用指南请参考：[UV_GUIDE.md](UV_GUIDE.md)

## 工具介绍

本工具包含以下文件：
- `pid_tuner.py` - 主要的PID调参GUI工具（增强版）
- `test_receiver.py` - 串口数据接收测试工具
- `protocol_doc.md` - 通信协议详细文档
- `pyproject.toml` - 项目配置文件（UV/pip兼容）
- `requirements.txt` - Python依赖列表（向后兼容）
- `UV_GUIDE.md` - UV包管理器详细使用指南

## 新增功能特性

### 🎯 自定义参数范围
- 每个PID参数都可以自定义最小值和最大值
- 实时更新滑块范围，精确控制参数调节
- 范围设置会自动保存到配置文件

### 🎛️ 增强的滑块控制
- 高精度滑块，支持小数点后5位精度
- 精度调节按钮（+/-按钮），可以进行0.001的微调
- 实时数值显示和输入框同步

### 📊 分页式界面
- **PID参数调节页面**：专注于参数调节操作
- **参数范围设置页面**：独立的范围配置界面

### 🔧 增强的功能按钮
- **推荐值**：一键设置每个环路的推荐起始参数
- **清零**：快速清零某个环路的所有参数
- **导出报告**：生成详细的参数调试报告

### 📦 现代化包管理
- 支持UV和pip两种包管理器
- 提供项目脚本命令，可直接运行
- 完整的开发环境配置

## 快速开始

### 1. 安装和运行
```bash
# 使用UV（推荐）
uv sync
uv run pid-tuner

# 或使用pip
pip install -r requirements.txt
python pid_tuner.py
```

### 2. 连接串口
- 在"串口设置"区域选择正确的COM端口
- 选择波特率（推荐115200）
- 点击"连接"按钮
- 观察连接状态指示灯（绿色=已连接，红色=未连接）

### 3. 设置参数范围（可选但推荐）
- 切换到"参数范围设置"页面
- 为每个参数设置合适的最小值和最大值
- 点击"应用"按钮更新滑块范围

**推荐范围设置：**
```
角速度环:
  P: 0.0 - 50.0 (可根据实际需要调整上限)
  I: 0.0 - 5.0
  D: 0.0 - 2.0

角度环:
  P: 0.0 - 20.0
  I: 0.0 - 2.0
  D: 0.0 - 1.0

速度环:
  P: 0.0 - 30.0
  I: 0.0 - 3.0
  D: 0.0 - 1.5
```

### 4. 调整PID参数
切换到"PID参数调节"页面：

#### 方法1：使用滑块
- 拖动滑块调节参数值
- 滑块会根据你设置的范围自动调整

#### 方法2：直接输入数值
- 在参数输入框中直接输入精确数值
- 支持小数点后5位精度

#### 方法3：精度微调
- 使用参数旁边的+/-按钮进行0.001的精细调节
- 适合最后的精细调参

#### 方法4：使用预设值
- 点击"推荐值"按钮快速设置起始参数
- 点击"清零"按钮快速清空参数

### 5. 参数发送和测试
- **单独发送**：点击每个环路的"发送"按钮
- **全部发送**：点击底部的"发送所有参数"按钮
- **实时观察**：通过状态信息查看发送日志

### 6. 配置管理
- **保存配置**：保存当前参数值和范围设置
- **加载配置**：从文件恢复之前的设置
- **导出报告**：生成详细的调参报告文档

## 开发环境设置

### 使用UV
```bash
# 安装开发依赖
uv sync --all-extras

# 代码格式化
uv run black .

# 代码检查
uv run flake8 .

# 类型检查
uv run mypy .
```

### 添加新依赖
```bash
# 添加运行时依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name
```

## 调参策略和技巧

### 🎯 推荐调参顺序
1. **第一步**：设置合适的参数范围
2. **第二步**：从角速度环开始调参
3. **第三步**：调节角度环
4. **第四步**：最后调节速度环

### 🔧 使用技巧

#### 快速开始
1. 点击"推荐值"设置起始参数
2. 发送参数观察效果
3. 根据响应情况微调

#### 精细调参
1. 使用滑块进行粗调
2. 使用输入框进行精确设置
3. 使用+/-按钮进行最终微调

#### 范围设置技巧
- 根据你的系统特性设置合适的范围
- P参数范围可以设置较大，方便快速找到合适区间
- I和D参数范围通常较小，避免系统不稳定

### 📊 参数效果分析
- **P参数过大**：系统震荡，响应过激
- **P参数过小**：响应迟缓，跟踪性能差
- **I参数过大**：超调严重，可能不稳定
- **I参数过小**：稳态误差大
- **D参数过大**：噪声放大，高频震荡
- **D参数过小**：超调，动态性能差

## 界面说明

### PID参数调节页面
- **参数标签**：显示P、I、D参数名称
- **范围显示**：显示当前参数的调节范围
- **滑块控制**：拖动调节参数值
- **数值输入**：精确输入参数值
- **精度调节**：+/-按钮进行微调
- **功能按钮**：发送、推荐值、清零

### 参数范围设置页面
- **最小值设置**：设置参数下限
- **最大值设置**：设置参数上限
- **应用按钮**：应用单个参数范围
- **应用全部**：应用整个环路的范围设置

## 导出报告功能

点击"导出参数报告"会生成包含以下信息的文档：
- 当前所有PID参数值
- 每个参数的调节范围
- 生成时间戳
- 便于记录和分析调参过程

## 故障排除

### 滑块不响应
- 检查参数范围设置是否合理
- 确保最小值小于最大值
- 重新应用范围设置

### 精度调节问题
- 精度调节步长为0.001
- 如果需要更大步长，可以直接在输入框修改

### 界面显示问题
- 调整窗口大小到1200x800或更大
- 使用滚动条查看完整内容

### UV相关问题
- 如果UV命令不工作，检查是否正确安装：`uv --version`
- 如果依赖安装失败，尝试：`uv sync --reinstall`
- 查看详细的UV使用指南：[UV_GUIDE.md](UV_GUIDE.md)

## C语言接收端示例代码

如果你需要在单片机或其他C语言环境中接收PID参数，可以参考以下示例代码：

### 数据结构定义

```c
#include <stdint.h>
#include <string.h>

// PID参数数据包结构（16字节）
typedef struct {
    uint8_t header[2];    // 帧头 0xA5 0x5A
    uint8_t type;         // 参数类型：0x01=角速度环, 0x02=角度环, 0x03=速度环
    float p;              // P参数（IEEE754单精度浮点数，小端序）
    float i;              // I参数
    float d;              // D参数  
    uint8_t checksum;     // 校验和
    uint8_t tail[2];      // 帧尾 0x5A 0xA5
} __attribute__((packed)) PIDPacket;

// PID参数存储结构
typedef struct {
    float p, i, d;
} PIDParams;

// 系统PID参数
PIDParams angular_velocity_pid = {0, 0, 0};  // 角速度环
PIDParams angle_pid = {0, 0, 0};             // 角度环  
PIDParams velocity_pid = {0, 0, 0};          // 速度环
```

### 数据包解析函数

```c
/**
 * 解析PID参数数据包
 * @param buffer: 接收到的数据缓冲区
 * @param len: 数据长度
 * @return: 1=成功解析, 0=无有效数据包
 */
int parse_pid_packet(uint8_t* buffer, int len) {
    // 查找完整的数据包（16字节）
    for (int i = 0; i <= len - 16; i++) {
        // 查找帧头 0xA5 0x5A
        if (buffer[i] == 0xA5 && buffer[i+1] == 0x5A) {
            PIDPacket* packet = (PIDPacket*)(buffer + i);
            
            // 验证帧尾 0x5A 0xA5
            if (packet->tail[0] == 0x5A && packet->tail[1] == 0xA5) {
                
                // 计算校验和
                uint8_t calculated_checksum = 0;
                for (int j = 2; j < 15; j++) {  // 从类型字节到D参数结束
                    calculated_checksum += buffer[i + j];
                }
                
                // 验证校验和
                if (calculated_checksum == packet->checksum) {
                    // 应用PID参数
                    apply_pid_params(packet->type, packet->p, packet->i, packet->d);
                    return 1;  // 成功解析
                }
            }
        }
    }
    return 0;  // 未找到有效数据包
}

/**
 * 应用接收到的PID参数
 * @param type: 参数类型
 * @param p, i, d: PID参数值
 */
void apply_pid_params(uint8_t type, float p, float i, float d) {
    switch (type) {
        case 0x01:  // 角速度环
            angular_velocity_pid.p = p;
            angular_velocity_pid.i = i;
            angular_velocity_pid.d = d;
            printf("更新角速度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
            
        case 0x02:  // 角度环
            angle_pid.p = p;
            angle_pid.i = i;
            angle_pid.d = d;
            printf("更新角度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
            
        case 0x03:  // 速度环
            velocity_pid.p = p;
            velocity_pid.i = i;
            velocity_pid.d = d;
            printf("更新速度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
            
        default:
            printf("未知参数类型: 0x%02X\n", type);
            break;
    }
}
```

### 串口接收处理示例

```c
#define BUFFER_SIZE 256

uint8_t rx_buffer[BUFFER_SIZE];
int rx_index = 0;

/**
 * 串口中断接收处理函数
 * @param data: 接收到的单个字节
 */
void uart_rx_handler(uint8_t data) {
    // 将接收到的数据存入缓冲区
    rx_buffer[rx_index] = data;
    rx_index++;
    
    // 防止缓冲区溢出
    if (rx_index >= BUFFER_SIZE) {
        rx_index = 0;
    }
    
    // 如果缓冲区有足够数据，尝试解析
    if (rx_index >= 16) {
        if (parse_pid_packet(rx_buffer, rx_index)) {
            // 成功解析后，移动缓冲区数据
            memmove(rx_buffer, rx_buffer + 16, rx_index - 16);
            rx_index -= 16;
        }
    }
}

/**
 * 主循环中的处理函数（轮询方式）
 */
void process_serial_data(void) {
    // 如果使用轮询方式接收串口数据
    while (uart_data_available()) {
        uint8_t data = uart_read_byte();
        uart_rx_handler(data);
    }
}
```

### STM32 HAL库示例

```c
// STM32 HAL库的串口接收中断处理
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart == &huart1) {  // 假设使用UART1
        uint8_t received_data;
        
        // 读取接收到的数据
        HAL_UART_Receive(&huart1, &received_data, 1, HAL_MAX_DELAY);
        
        // 处理接收数据
        uart_rx_handler(received_data);
        
        // 重新启动接收中断
        HAL_UART_Receive_IT(&huart1, &received_data, 1);
    }
}
```

### 使用示例

```c
int main(void) {
    // 系统初始化
    system_init();
    uart_init(115200);  // 初始化串口，波特率115200
    
    printf("PID参数接收器已启动\n");
    printf("等待接收PID参数...\n");
    
    while (1) {
        // 主循环处理
        process_serial_data();
        
        // 其他系统任务
        // control_loop();  // 执行控制算法
        
        delay_ms(1);
    }
}
```

### 编译注意事项

1. **字节对齐**：确保结构体按字节对齐，使用 `__attribute__((packed))`
2. **端序问题**：IEEE754浮点数使用小端序，确保处理器字节序匹配
3. **缓冲区管理**：合理设置接收缓冲区大小，防止溢出
4. **实时性**：建议在中断中接收数据，主循环中解析数据包

### 数据包格式说明

```
+--------+--------+------+--------+--------+--------+----------+--------+--------+
| 帧头1  | 帧头2  | 类型 |   P    |   I    |   D    |  校验和  | 帧尾1  | 帧尾2  |
+--------+--------+------+--------+--------+--------+----------+--------+--------+
| 0xA5   | 0x5A   | 1字节| 4字节  | 4字节  | 4字节  |  1字节   | 0x5A   | 0xA5   |
+--------+--------+------+--------+--------+--------+----------+--------+--------+
```

- **帧头**: 0xA5 0x5A（固定值）
- **类型**: 0x01=角速度环, 0x02=角度环, 0x03=速度环
- **PID参数**: IEEE754单精度浮点数，小端序
- **校验和**: (类型 + P的4字节 + I的4字节 + D的4字节) 的和 & 0xFF
- **帧尾**: 0x5A 0xA5（固定值）

这个C语言示例代码可以直接在单片机项目中使用，根据你的具体硬件平台调整串口初始化和数据接收部分即可。

## 技术支持

如需技术支持，请提供：
1. 错误现象描述
2. 使用的参数值和范围设置
3. 串口配置信息
4. 状态信息区域的错误日志
5. 导出的参数报告（如有）
6. 使用的包管理器（UV或pip）和版本信息