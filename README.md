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

### 方法一：结构体方式（原方法）

```c
#include <stdint.h>
#include <string.h>

// PID参数数据包结构（17字节）
typedef struct {
    uint8_t header;       // 帧头 0xA5
    uint8_t command;      // 指令字：0x01=角速度环, 0x02=角度环, 0x03=速度环
    float p;              // P参数（IEEE754单精度浮点数，小端序）
    float i;              // I参数
    float d;              // D参数  
    uint8_t checksum;     // 校验和
} __attribute__((packed)) PIDPacket;
```

### 方法二：Union联合体方式（推荐）

```c
#include <stdint.h>
#include <string.h>

// 使用union进行数据包解析，更灵活和高效
typedef union {
    // 按字节访问整个数据包
    uint8_t bytes[17];
    
    // 按结构化方式访问
    struct {
        uint8_t header;       // 帧头 0xA5
        uint8_t command;      // 指令字
        float p;              // P参数
        float i;              // I参数
        float d;              // D参数
        uint8_t checksum;     // 校验和
    } __attribute__((packed)) fields;
    
    // 按不同数据类型分组访问
    struct {
        uint8_t header_cmd[2];    // 帧头+指令字
        float params[3];          // P、I、D参数数组
        uint8_t checksum;         // 校验和
    } __attribute__((packed)) groups;
    
} PIDPacketUnion;

// 浮点数与字节转换的union
typedef union {
    float f;
    uint8_t bytes[4];
    uint32_t u32;
} FloatUnion;

// PID参数存储结构
typedef struct {
    float p, i, d;
} PIDParams;

// 系统PID参数
PIDParams angular_velocity_pid = {0, 0, 0};  // 角速度环
PIDParams angle_pid = {0, 0, 0};             // 角度环  
PIDParams velocity_pid = {0, 0, 0};          // 速度环
```

### Union方式的数据包解析函数

```c
/**
 * 使用Union解析PID参数数据包
 * @param buffer: 接收到的数据缓冲区
 * @param len: 数据长度
 * @return: 1=成功解析, 0=无有效数据包
 */
int parse_pid_packet_union(uint8_t* buffer, int len) {
    PIDPacketUnion packet;
    
    // 查找完整的数据包（17字节）
    for (int i = 0; i <= len - 17; i++) {
        // 查找帧头 0xA5
        if (buffer[i] == 0xA5) {
            
            // 将数据复制到union中
            memcpy(packet.bytes, &buffer[i], 17);
            
            // 验证指令字有效性
            if (packet.fields.command >= 0x01 && packet.fields.command <= 0x03) {
                
                // 使用Union方式计算校验和
                uint8_t calculated_checksum = 0;
                for (int j = 1; j < 16; j++) {  // 从指令字到D参数结束
                    calculated_checksum += packet.bytes[j];
                }
                
                // 验证校验和
                if (calculated_checksum == packet.fields.checksum) {
                    // 应用PID参数 - 直接使用union的结构化访问
                    apply_pid_params_union(&packet);
                    return 1;  // 成功解析
                }
            }
        }
    }
    return 0;  // 未找到有效数据包
}

/**
 * 应用接收到的PID参数（Union版本）
 * @param packet: 数据包Union指针
 */
void apply_pid_params_union(PIDPacketUnion* packet) {
    // 可以用多种方式访问数据
    uint8_t command = packet->fields.command;
    float p = packet->fields.p;  // 或者 packet->groups.params[0]
    float i = packet->fields.i;  // 或者 packet->groups.params[1]
    float d = packet->fields.d;  // 或者 packet->groups.params[2]
    
    switch (command) {
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
            printf("未知指令字: 0x%02X\n", command);
            break;
    }
}
```

### 高级Union用法：字节序转换

```c
/**
 * 处理字节序转换的增强版解析函数
 * 适用于大端序处理器或需要字节序转换的场合
 */
int parse_pid_packet_endian_safe(uint8_t* buffer, int len) {
    PIDPacketUnion packet;
    FloatUnion float_converter;
    
    for (int i = 0; i <= len - 17; i++) {
        if (buffer[i] == 0xA5) {
            memcpy(packet.bytes, &buffer[i], 17);
            
            if (packet.fields.command >= 0x01 && packet.fields.command <= 0x03) {
                
                // 校验和计算
                uint8_t calculated_checksum = 0;
                for (int j = 1; j < 16; j++) {
                    calculated_checksum += packet.bytes[j];
                }
                
                if (calculated_checksum == packet.fields.checksum) {
                    
                    // 如果需要字节序转换（大端序系统）
                    #ifdef BIG_ENDIAN_SYSTEM
                    // 转换P参数
                    for (int k = 0; k < 4; k++) {
                        float_converter.bytes[k] = packet.bytes[2 + 3 - k];
                    }
                    float p = float_converter.f;
                    
                    // 转换I参数
                    for (int k = 0; k < 4; k++) {
                        float_converter.bytes[k] = packet.bytes[6 + 3 - k];
                    }
                    float i = float_converter.f;
                    
                    // 转换D参数
                    for (int k = 0; k < 4; k++) {
                        float_converter.bytes[k] = packet.bytes[10 + 3 - k];
                    }
                    float d = float_converter.f;
                    #else
                    // 小端序系统，直接使用
                    float p = packet.fields.p;
                    float i = packet.fields.i;
                    float d = packet.fields.d;
                    #endif
                    
                    // 应用参数
                    apply_pid_params_direct(packet.fields.command, p, i, d);
                    return 1;
                }
            }
        }
    }
    return 0;
}

/**
 * 直接参数应用函数
 */
void apply_pid_params_direct(uint8_t command, float p, float i, float d) {
    switch (command) {
        case 0x01:
            angular_velocity_pid.p = p;
            angular_velocity_pid.i = i;
            angular_velocity_pid.d = d;
            printf("更新角速度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
        case 0x02:
            angle_pid.p = p;
            angle_pid.i = i;
            angle_pid.d = d;
            printf("更新角度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
        case 0x03:
            velocity_pid.p = p;
            velocity_pid.i = i;
            velocity_pid.d = d;
            printf("更新速度环PID: P=%.5f, I=%.5f, D=%.5f\n", p, i, d);
            break;
        default:
            printf("未知指令字: 0x%02X\n", command);
            break;
    }
}
```

### 流式解析器（状态机+Union）

```c
// 解析状态枚举
typedef enum {
    PARSE_STATE_WAIT_HEADER,
    PARSE_STATE_WAIT_COMMAND,
    PARSE_STATE_WAIT_DATA,
    PARSE_STATE_WAIT_CHECKSUM,
    PARSE_STATE_COMPLETE
} ParseState;

// 流式解析器结构
typedef struct {
    ParseState state;
    PIDPacketUnion packet;
    int byte_index;
    uint8_t calculated_checksum;
} StreamParser;

// 初始化解析器
void init_stream_parser(StreamParser* parser) {
    parser->state = PARSE_STATE_WAIT_HEADER;
    parser->byte_index = 0;
    parser->calculated_checksum = 0;
    memset(&parser->packet, 0, sizeof(PIDPacketUnion));
}

/**
 * 流式解析单个字节
 * @param parser: 解析器指针
 * @param byte: 接收到的字节
 * @return: 1=数据包完成, 0=需要更多数据, -1=错误
 */
int parse_stream_byte(StreamParser* parser, uint8_t byte) {
    switch (parser->state) {
        case PARSE_STATE_WAIT_HEADER:
            if (byte == 0xA5) {
                parser->packet.bytes[0] = byte;
                parser->byte_index = 1;
                parser->calculated_checksum = 0;
                parser->state = PARSE_STATE_WAIT_COMMAND;
            }
            break;
            
        case PARSE_STATE_WAIT_COMMAND:
            if (byte >= 0x01 && byte <= 0x03) {
                parser->packet.bytes[1] = byte;
                parser->calculated_checksum += byte;
                parser->byte_index = 2;
                parser->state = PARSE_STATE_WAIT_DATA;
            } else {
                parser->state = PARSE_STATE_WAIT_HEADER;
                return -1;
            }
            break;
            
        case PARSE_STATE_WAIT_DATA:
            parser->packet.bytes[parser->byte_index] = byte;
            parser->calculated_checksum += byte;
            parser->byte_index++;
            
            if (parser->byte_index == 16) {  // 收集完所有数据
                parser->state = PARSE_STATE_WAIT_CHECKSUM;
            }
            break;
            
        case PARSE_STATE_WAIT_CHECKSUM:
            parser->packet.bytes[16] = byte;
            
            if ((parser->calculated_checksum & 0xFF) == byte) {
                parser->state = PARSE_STATE_COMPLETE;
                return 1;  // 数据包完成
            } else {
                parser->state = PARSE_STATE_WAIT_HEADER;
                return -1;  // 校验和错误
            }
            break;
            
        case PARSE_STATE_COMPLETE:
            // 重置解析器
            parser->state = PARSE_STATE_WAIT_HEADER;
            break;
    }
    
    return 0;  // 需要更多数据
}
```

### 使用示例

```c
// 全局解析器
StreamParser g_parser;

/**
 * 串口中断接收处理函数（使用流式解析器）
 */
void uart_rx_handler_stream(uint8_t data) {
    int result = parse_stream_byte(&g_parser, data);
    
    if (result == 1) {
        // 数据包解析完成
        apply_pid_params_union(&g_parser.packet);
        
        // 打印调试信息
        printf("收到数据包: ");
        for (int i = 0; i < 17; i++) {
            printf("%02X ", g_parser.packet.bytes[i]);
        }
        printf("\n");
        
    } else if (result == -1) {
        // 解析错误
        printf("数据包解析错误\n");
    }
    // result == 0 时继续等待更多数据
}

/**
 * 主函数示例
 */
int main(void) {
    // 系统初始化
    system_init();
    uart_init(115200);
    
    // 初始化解析器
    init_stream_parser(&g_parser);
    
    printf("PID参数接收器已启动（Union版本）\n");
    printf("支持流式解析和多种数据访问方式\n");
    
    while (1) {
        // 主循环处理
        // uart_rx_handler_stream() 会在中断中被调用
        
        // 其他系统任务
        delay_ms(1);
    }
}
```

### Union方式的优势

1. **灵活的数据访问**：
   - `packet.bytes[i]` - 按字节访问
   - `packet.fields.p` - 按结构化字段访问
   - `packet.groups.params[0]` - 按分组访问

2. **内存效率**：
   - 同一块内存的不同视图
   - 零拷贝数据转换
   - 减少内存占用

3. **类型安全**：
   - 编译时类型检查
   - 避免指针转换错误

4. **易于调试**：
   - 可以同时查看原始字节和解析后的数据
   - 方便打印和分析

5. **字节序处理**：
   - 灵活处理不同字节序
   - 支持跨平台移植

这种Union方式特别适合需要高效解析二进制协议的嵌入式系统！