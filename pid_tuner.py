import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import json
import struct
import threading
import time

class PIDTuner:
    def __init__(self, root):
        self.root = root
        self.root.title("PID调参工具 - 底盘控制")
        self.root.geometry("1200x800")
        
        # 串口连接
        self.serial_port = None
        self.is_connected = False
        
        # PID参数
        self.pid_params = {
            'angular_velocity': {'P': 0.0, 'I': 0.0, 'D': 0.0},
            'angle': {'P': 0.0, 'I': 0.0, 'D': 0.0},
            'velocity': {'P': 0.0, 'I': 0.0, 'D': 0.0}
        }
        
        # 参数范围设置 (默认值)
        self.param_ranges = {
            'angular_velocity': {
                'P': {'min': 0.0, 'max': 50.0},
                'I': {'min': 0.0, 'max': 5.0},
                'D': {'min': 0.0, 'max': 2.0}
            },
            'angle': {
                'P': {'min': 0.0, 'max': 20.0},
                'I': {'min': 0.0, 'max': 2.0},
                'D': {'min': 0.0, 'max': 1.0}
            },
            'velocity': {
                'P': {'min': 0.0, 'max': 30.0},
                'I': {'min': 0.0, 'max': 3.0},
                'D': {'min': 0.0, 'max': 1.5}
            }
        }
        
        self.setup_ui()
        self.update_port_list()
        
    def setup_ui(self):
        # 配置窗口网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 主容器
        main_container = ttk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # 串口连接区域
        self.setup_serial_frame(main_container)
        
        # 主要内容区域 - 使用Notebook分页
        notebook = ttk.Notebook(main_container)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # PID参数调节页面
        pid_frame = ttk.Frame(notebook)
        notebook.add(pid_frame, text="PID参数调节")
        self.setup_pid_frame(pid_frame)
        
        # 参数范围设置页面
        range_frame = ttk.Frame(notebook)
        notebook.add(range_frame, text="参数范围设置")
        self.setup_range_frame(range_frame)
        
        # 控制和状态区域
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.setup_control_frame(bottom_frame)
        self.setup_status_frame(bottom_frame)
        
    def setup_serial_frame(self, parent):
        serial_frame = ttk.LabelFrame(parent, text="串口设置", padding="10")
        serial_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 端口选择
        ttk.Label(serial_frame, text="端口:").grid(row=0, column=0, padx=(0, 5))
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(serial_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=(0, 10))
        
        # 波特率选择
        ttk.Label(serial_frame, text="波特率:").grid(row=0, column=2, padx=(0, 5))
        self.baud_var = tk.StringVar(value="115200")
        baud_combo = ttk.Combobox(serial_frame, textvariable=self.baud_var, 
                                 values=["9600", "19200", "38400", "57600", "115200"], width=10)
        baud_combo.grid(row=0, column=3, padx=(0, 10))
        
        # 连接按钮
        self.connect_btn = ttk.Button(serial_frame, text="连接", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=4, padx=5)
        
        # 刷新端口按钮
        ttk.Button(serial_frame, text="刷新", command=self.update_port_list).grid(row=0, column=5)
        
        # 连接状态指示
        self.status_label = ttk.Label(serial_frame, text="未连接", foreground="red")
        self.status_label.grid(row=0, column=6, padx=(10, 0))
        
    def setup_pid_frame(self, parent):
        # 创建滚动框架
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # PID控制组
        self.pid_controls = {}
        
        # 角速度环
        self.create_pid_group(scrollable_frame, "角速度环 (Angular Velocity)", 'angular_velocity', 0)
        
        # 角度环
        self.create_pid_group(scrollable_frame, "角度环 (Angle)", 'angle', 1)
        
        # 速度环
        self.create_pid_group(scrollable_frame, "速度环 (Velocity)", 'velocity', 2)
        
    def create_pid_group(self, parent, title, param_key, row):
        # 主框架
        group_frame = ttk.LabelFrame(parent, text=title, padding="15")
        group_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=10, padx=10)
        group_frame.grid_columnconfigure(2, weight=1)
        
        # 创建参数控制
        self.pid_controls[param_key] = {}
        
        pid_types = ['P', 'I', 'D']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # 不同颜色区分P、I、D
        
        for i, (pid_type, color) in enumerate(zip(pid_types, colors)):
            # 参数标签
            label = ttk.Label(group_frame, text=f"{pid_type}参数:", font=('Arial', 10, 'bold'))
            label.grid(row=i, column=0, sticky=tk.W, pady=5)
            
            # 范围显示
            range_info = self.param_ranges[param_key][pid_type]
            range_label = ttk.Label(group_frame, text=f"[{range_info['min']:.1f} - {range_info['max']:.1f}]")
            range_label.grid(row=i, column=1, padx=(5, 10))
            
            # 滑块
            var = tk.DoubleVar()
            scale = ttk.Scale(group_frame, 
                            from_=range_info['min'], 
                            to=range_info['max'], 
                            variable=var, 
                            orient=tk.HORIZONTAL, 
                            length=300)
            scale.grid(row=i, column=2, sticky=(tk.W, tk.E), padx=5)
            
            # 数值输入框
            entry = ttk.Entry(group_frame, textvariable=var, width=10)
            entry.grid(row=i, column=3, padx=5)
            
            # 精度调节按钮
            precision_frame = ttk.Frame(group_frame)
            precision_frame.grid(row=i, column=4, padx=5)
            
            ttk.Button(precision_frame, text="-", width=3,
                      command=lambda v=var: self.adjust_precision(v, -0.001)).grid(row=0, column=0)
            ttk.Button(precision_frame, text="+", width=3,
                      command=lambda v=var: self.adjust_precision(v, 0.001)).grid(row=0, column=1)
            
            # 存储控件引用
            self.pid_controls[param_key][pid_type] = {
                'var': var,
                'scale': scale,
                'entry': entry,
                'range_label': range_label
            }
            
            # 绑定变量更新事件
            var.trace('w', lambda *args, pt=param_key, pid=pid_type: self.update_pid_param(pt, pid, var.get()))
            
        # 发送按钮
        send_frame = ttk.Frame(group_frame)
        send_frame.grid(row=len(pid_types), column=0, columnspan=5, pady=10)
        
        ttk.Button(send_frame, text=f"发送 {title}", 
                  command=lambda: self.send_pid_params(param_key)).grid(row=0, column=0, padx=5)
        
        # 预设值按钮
        ttk.Button(send_frame, text="推荐值", 
                  command=lambda: self.set_recommended_values(param_key)).grid(row=0, column=1, padx=5)
        
        ttk.Button(send_frame, text="清零", 
                  command=lambda: self.clear_values(param_key)).grid(row=0, column=2, padx=5)
        
    def setup_range_frame(self, parent):
        # 范围设置标题
        title_label = ttk.Label(parent, text="参数范围设置", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # 创建范围设置控件
        self.range_controls = {}
        
        loop_names = [
            ('angular_velocity', '角速度环'),
            ('angle', '角度环'), 
            ('velocity', '速度环')
        ]
        
        for i, (param_key, display_name) in enumerate(loop_names):
            self.create_range_group(parent, display_name, param_key, i+1)
            
    def create_range_group(self, parent, title, param_key, row):
        group_frame = ttk.LabelFrame(parent, text=title, padding="10")
        group_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=5, padx=20)
        
        self.range_controls[param_key] = {}
        
        # 表头
        ttk.Label(group_frame, text="参数", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        ttk.Label(group_frame, text="最小值", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5)
        ttk.Label(group_frame, text="最大值", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)
        ttk.Label(group_frame, text="操作", font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=5)
        
        for i, pid_type in enumerate(['P', 'I', 'D']):
            row_idx = i + 1
            
            # 参数名
            ttk.Label(group_frame, text=pid_type).grid(row=row_idx, column=0, padx=5, pady=2)
            
            # 最小值输入
            min_var = tk.DoubleVar(value=self.param_ranges[param_key][pid_type]['min'])
            min_entry = ttk.Entry(group_frame, textvariable=min_var, width=10)
            min_entry.grid(row=row_idx, column=1, padx=5, pady=2)
            
            # 最大值输入
            max_var = tk.DoubleVar(value=self.param_ranges[param_key][pid_type]['max'])
            max_entry = ttk.Entry(group_frame, textvariable=max_var, width=10)
            max_entry.grid(row=row_idx, column=2, padx=5, pady=2)
            
            # 应用按钮
            apply_btn = ttk.Button(group_frame, text="应用", 
                                 command=lambda pk=param_key, pt=pid_type, minv=min_var, maxv=max_var: 
                                 self.apply_range(pk, pt, minv.get(), maxv.get()))
            apply_btn.grid(row=row_idx, column=3, padx=5, pady=2)
            
            self.range_controls[param_key][pid_type] = {
                'min_var': min_var,
                'max_var': max_var,
                'min_entry': min_entry,
                'max_entry': max_entry
            }
            
        # 全部应用按钮
        apply_all_btn = ttk.Button(group_frame, text="应用全部", 
                                 command=lambda pk=param_key: self.apply_all_ranges(pk))
        apply_all_btn.grid(row=4, column=0, columnspan=4, pady=10)
        
    def setup_control_frame(self, parent):
        control_frame = ttk.LabelFrame(parent, text="控制操作", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 全部发送
        ttk.Button(control_frame, text="发送所有参数", 
                  command=self.send_all_params).grid(row=0, column=0, padx=5)
        
        # 保存配置
        ttk.Button(control_frame, text="保存配置", 
                  command=self.save_config).grid(row=0, column=1, padx=5)
        
        # 加载配置
        ttk.Button(control_frame, text="加载配置", 
                  command=self.load_config).grid(row=0, column=2, padx=5)
        
        # 重置参数
        ttk.Button(control_frame, text="重置参数", 
                  command=self.reset_params).grid(row=0, column=3, padx=5)
        
        # 导出报告
        ttk.Button(control_frame, text="导出参数报告", 
                  command=self.export_report).grid(row=0, column=4, padx=5)
        
    def setup_status_frame(self, parent):
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="5")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态文本框
        self.status_text = tk.Text(status_frame, height=6, width=80)
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)
        
    def adjust_precision(self, var, delta):
        """精度调节"""
        current = var.get()
        new_value = current + delta
        var.set(round(new_value, 6))
        
    def apply_range(self, param_key, pid_type, min_val, max_val):
        """应用单个参数范围"""
        if min_val >= max_val:
            messagebox.showerror("错误", "最小值必须小于最大值")
            return
            
        self.param_ranges[param_key][pid_type]['min'] = min_val
        self.param_ranges[param_key][pid_type]['max'] = max_val
        
        # 更新滑块范围
        scale = self.pid_controls[param_key][pid_type]['scale']
        scale.configure(from_=min_val, to=max_val)
        
        # 更新范围显示
        range_label = self.pid_controls[param_key][pid_type]['range_label']
        range_label.config(text=f"[{min_val:.1f} - {max_val:.1f}]")
        
        self.log_status(f"已更新 {param_key} {pid_type} 参数范围: [{min_val:.3f} - {max_val:.3f}]")
        
    def apply_all_ranges(self, param_key):
        """应用某个环路的所有参数范围"""
        for pid_type in ['P', 'I', 'D']:
            controls = self.range_controls[param_key][pid_type]
            min_val = controls['min_var'].get()
            max_val = controls['max_var'].get()
            self.apply_range(param_key, pid_type, min_val, max_val)
            
    def set_recommended_values(self, param_key):
        """设置推荐值"""
        recommended = {
            'angular_velocity': {'P': 10.0, 'I': 0.1, 'D': 0.01},
            'angle': {'P': 5.0, 'I': 0.05, 'D': 0.1},
            'velocity': {'P': 8.0, 'I': 0.2, 'D': 0.05}
        }
        
        if param_key in recommended:
            for pid_type, value in recommended[param_key].items():
                self.pid_controls[param_key][pid_type]['var'].set(value)
            self.log_status(f"已设置 {param_key} 推荐参数值")
            
    def clear_values(self, param_key):
        """清零参数"""
        for pid_type in ['P', 'I', 'D']:
            self.pid_controls[param_key][pid_type]['var'].set(0.0)
        self.log_status(f"已清零 {param_key} 参数")
        
    def export_report(self):
        """导出参数报告"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"pid_report_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PID参数调试报告\n")
                f.write("=" * 50 + "\n")
                f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for param_key, display_name in [('angular_velocity', '角速度环'), 
                                              ('angle', '角度环'), 
                                              ('velocity', '速度环')]:
                    f.write(f"{display_name}:\n")
                    params = self.pid_params[param_key]
                    ranges = self.param_ranges[param_key]
                    
                    for pid_type in ['P', 'I', 'D']:
                        value = params[pid_type]
                        range_info = ranges[pid_type]
                        f.write(f"  {pid_type}: {value:.6f} (范围: {range_info['min']:.1f} - {range_info['max']:.1f})\n")
                    f.write("\n")
                    
            self.log_status(f"参数报告已导出到: {filename}")
            messagebox.showinfo("提示", f"报告已保存为: {filename}")
            
        except Exception as e:
            self.log_status(f"导出报告失败: {str(e)}")
            
    def update_port_list(self):
        """更新可用串口列表"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports and not self.port_var.get():
            self.port_var.set(ports[0])
            
    def toggle_connection(self):
        """切换串口连接状态"""
        if not self.is_connected:
            self.connect_serial()
        else:
            self.disconnect_serial()
            
    def connect_serial(self):
        """连接串口"""
        try:
            port = self.port_var.get()
            baud = int(self.baud_var.get())
            
            if not port:
                messagebox.showerror("错误", "请选择串口")
                return
                
            self.serial_port = serial.Serial(port, baud, timeout=1)
            self.is_connected = True
            self.connect_btn.config(text="断开")
            self.status_label.config(text="已连接", foreground="green")
            self.log_status(f"已连接到 {port}, 波特率 {baud}")
            
        except Exception as e:
            messagebox.showerror("连接错误", f"无法连接串口: {str(e)}")
            self.log_status(f"连接失败: {str(e)}")
            
    def disconnect_serial(self):
        """断开串口连接"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.is_connected = False
        self.connect_btn.config(text="连接")
        self.status_label.config(text="未连接", foreground="red")
        self.log_status("串口已断开")
        
    def update_pid_param(self, param_type, pid_type, value):
        """更新PID参数"""
        self.pid_params[param_type][pid_type] = value
        
    def send_pid_params(self, param_type):
        """发送指定类型的PID参数"""
        if not self.is_connected:
            messagebox.showwarning("警告", "请先连接串口")
            return
            
        try:
            params = self.pid_params[param_type]
            self.send_data(param_type, params['P'], params['I'], params['D'])
            self.log_status(f"已发送 {param_type} PID参数: P={params['P']:.3f}, I={params['I']:.3f}, D={params['D']:.3f}")
        except Exception as e:
            self.log_status(f"发送参数失败: {str(e)}")
            
    def send_all_params(self):
        """发送所有PID参数"""
        if not self.is_connected:
            messagebox.showwarning("警告", "请先连接串口")
            return
            
        for param_type in self.pid_params:
            self.send_pid_params(param_type)
            time.sleep(0.1)  # 短暂延时避免发送过快
            
    def send_data(self, param_type, p, i, d):
        """发送数据到串口"""
        # 通信协议格式：
        # 帧头(2字节) + 类型(1字节) + P(4字节float) + I(4字节float) + D(4字节float) + 校验和(1字节) + 帧尾(2字节)
        
        frame_header = b'\xAA\x55'  # 帧头
        frame_tail = b'\x55\xAA'   # 帧尾
        
        # 参数类型映射
        type_map = {
            'angular_velocity': 0x01,  # 角速度环
            'angle': 0x02,            # 角度环
            'velocity': 0x03          # 速度环
        }
        
        param_type_byte = bytes([type_map[param_type]])
        
        # 打包浮点数参数
        p_bytes = struct.pack('<f', p)
        i_bytes = struct.pack('<f', i)
        d_bytes = struct.pack('<f', d)
        
        # 计算校验和
        data_bytes = param_type_byte + p_bytes + i_bytes + d_bytes
        checksum = sum(data_bytes) & 0xFF
        checksum_byte = bytes([checksum])
        
        # 组装完整数据包
        packet = frame_header + data_bytes + checksum_byte + frame_tail
        
        # 发送数据
        self.serial_port.write(packet)
        
    def save_config(self):
        """保存配置到文件"""
        try:
            config_data = {
                'pid_params': self.pid_params,
                'param_ranges': self.param_ranges
            }
            with open('pid_config.json', 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            self.log_status("配置已保存到 pid_config.json")
            messagebox.showinfo("提示", "配置保存成功")
        except Exception as e:
            self.log_status(f"保存配置失败: {str(e)}")
            
    def load_config(self):
        """从文件加载配置"""
        try:
            with open('pid_config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # 兼容旧格式
            if 'pid_params' in config_data:
                self.pid_params.update(config_data['pid_params'])
                if 'param_ranges' in config_data:
                    self.param_ranges.update(config_data['param_ranges'])
            else:
                # 旧格式兼容
                self.pid_params.update(config_data)
                
            # 更新界面
            for param_type, controls in self.pid_controls.items():
                if param_type in self.pid_params:
                    for pid_type in ['P', 'I', 'D']:
                        value = self.pid_params[param_type][pid_type]
                        controls[pid_type]['var'].set(value)
                        
            # 更新范围控件
            if hasattr(self, 'range_controls'):
                for param_type, controls in self.range_controls.items():
                    if param_type in self.param_ranges:
                        for pid_type in ['P', 'I', 'D']:
                            range_info = self.param_ranges[param_type][pid_type]
                            controls[pid_type]['min_var'].set(range_info['min'])
                            controls[pid_type]['max_var'].set(range_info['max'])
                            
            self.log_status("配置已从 pid_config.json 加载")
            messagebox.showinfo("提示", "配置加载成功")
        except FileNotFoundError:
            messagebox.showwarning("警告", "配置文件不存在")
        except Exception as e:
            self.log_status(f"加载配置失败: {str(e)}")
            
    def reset_params(self):
        """重置所有参数为0"""
        for param_type, controls in self.pid_controls.items():
            for pid_type in ['P', 'I', 'D']:
                controls[pid_type]['var'].set(0.0)
        self.log_status("所有参数已重置为0")
        
    def log_status(self, message):
        """记录状态信息"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.status_text.insert(tk.END, log_message)
        self.status_text.see(tk.END)
        
    def on_closing(self):
        """关闭程序时的清理工作"""
        if self.is_connected:
            self.disconnect_serial()
        self.root.destroy()

def main():
    """主函数入口"""
    root = tk.Tk()
    app = PIDTuner(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()