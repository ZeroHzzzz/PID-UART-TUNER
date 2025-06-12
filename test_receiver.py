import serial
import serial.tools.list_ports
import struct
import time

class PIDReceiver:
    def __init__(self):
        self.serial_port = None
        self.is_running = False
        
    def list_ports(self):
        """列出可用串口"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        print("可用串口:")
        for i, port in enumerate(ports):
            print(f"{i+1}. {port}")
        return ports
        
    def connect(self, port, baud=115200):
        """连接串口"""
        try:
            self.serial_port = serial.Serial(port, baud, timeout=1)
            print(f"已连接到 {port}, 波特率 {baud}")
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
            
    def disconnect(self):
        """断开连接"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("串口已断开")
            
    def parse_packet(self, data):
        """解析数据包"""
        if len(data) != 16:
            return None
            
        # 检查帧头和帧尾
        if data[0:2] != b'\xA5\x5A' or data[14:16] != b'\x5A\xA5':
            return None
            
        # 提取数据
        param_type = data[2]
        p_bytes = data[3:7]
        i_bytes = data[7:11]
        d_bytes = data[11:15]
        checksum = data[13]
        
        # 验证校验和
        data_for_checksum = data[2:13]
        calculated_checksum = sum(data_for_checksum) & 0xFF
        if calculated_checksum != checksum:
            print(f"校验和错误: 期望 {checksum:02X}, 计算得 {calculated_checksum:02X}")
            return None
            
        # 解析浮点数
        try:
            p = struct.unpack('<f', p_bytes)[0]
            i = struct.unpack('<f', i_bytes)[0]
            d = struct.unpack('<f', d_bytes)[0]
        except:
            print("浮点数解析失败")
            return None
            
        # 参数类型映射
        type_names = {
            0x01: "角速度环",
            0x02: "角度环", 
            0x03: "速度环"
        }
        
        return {
            'type': type_names.get(param_type, f"未知类型({param_type:02X})"),
            'P': p,
            'I': i,
            'D': d
        }
        
    def listen(self):
        """监听串口数据"""
        if not self.serial_port or not self.serial_port.is_open:
            print("串口未连接")
            return
            
        print("开始监听串口数据... (按Ctrl+C停止)")
        self.is_running = True
        buffer = b''
        
        try:
            while self.is_running:
                if self.serial_port.in_waiting > 0:
                    # 读取数据
                    new_data = self.serial_port.read(self.serial_port.in_waiting)
                    buffer += new_data
                    
                    # 查找完整的数据包
                    while len(buffer) >= 16:
                        # 查找帧头
                        start_index = buffer.find(b'\xA5\x5A')
                        if start_index == -1:
                            buffer = buffer[-1:]  # 保留最后一个字节
                            break
                            
                        # 移除帧头之前的数据
                        if start_index > 0:
                            buffer = buffer[start_index:]
                            
                        # 检查是否有完整的数据包
                        if len(buffer) >= 16:
                            packet = buffer[:16]
                            buffer = buffer[16:]
                            
                            # 解析数据包
                            result = self.parse_packet(packet)
                            if result:
                                timestamp = time.strftime("%H:%M:%S")
                                print(f"[{timestamp}] 接收到 {result['type']} PID参数:")
                                print(f"  P = {result['P']:.5f}")
                                print(f"  I = {result['I']:.5f}")
                                print(f"  D = {result['D']:.5f}")
                                print("-" * 40)
                            else:
                                print("接收到无效数据包")
                                # 打印原始数据用于调试
                                hex_str = ' '.join(f'{b:02X}' for b in packet)
                                print(f"原始数据: {hex_str}")
                                print("-" * 40)
                        else:
                            break
                            
                time.sleep(0.01)  # 短暂延时
                
        except KeyboardInterrupt:
            print("\n停止监听")
        except Exception as e:
            print(f"监听过程中出错: {e}")
        finally:
            self.is_running = False

def main():
    """主函数入口"""
    receiver = PIDReceiver()
    
    # 列出可用端口
    ports = receiver.list_ports()
    if not ports:
        print("未找到可用串口")
        return
        
    # 选择端口
    while True:
        try:
            choice = input(f"\n请选择串口 (1-{len(ports)}, 或输入端口名): ").strip()
            if choice.isdigit():
                port_index = int(choice) - 1
                if 0 <= port_index < len(ports):
                    selected_port = ports[port_index]
                    break
            else:
                selected_port = choice
                break
        except (ValueError, IndexError):
            print("无效选择，请重新输入")
            
    # 选择波特率  
    baud_rates = [9600, 19200, 38400, 57600, 115200]
    print(f"\n可用波特率: {baud_rates}")
    baud_input = input("请选择波特率 (默认115200): ").strip()
    if baud_input.isdigit() and int(baud_input) in baud_rates:
        selected_baud = int(baud_input)
    else:
        selected_baud = 115200
        
    # 连接并开始监听
    if receiver.connect(selected_port, selected_baud):
        try:
            receiver.listen()
        finally:
            receiver.disconnect()
    else:
        print("连接失败，程序退出")

if __name__ == "__main__":
    main()