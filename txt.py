import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

class NovelReader:
    def __init__(self, root):
        self.root = root
        self.root.title("本地 TXT 小说阅读器")
        self.root.geometry("800x600")

        # 初始化变量
        self.current_page = 0
        self.pages = []
        self.font_size = 12
        self.font_family = "Arial"
        self.bg_color = "white"
        self.text_color = "black"
        # 新增字体间距变量，初始值为 0
        self.line_spacing = 0

        # 创建菜单栏
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="打开", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.root.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)

        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="字体大小", command=self.change_font_size)
        self.view_menu.add_command(label="选择字体", command=self.change_font_family)
        self.view_menu.add_command(label="背景颜色", command=self.change_bg_color)
        self.view_menu.add_command(label="文字颜色", command=self.change_text_color)
        # 新增调整字体间距菜单项
        self.view_menu.add_command(label="字体间距", command=self.change_line_spacing)
        self.menu_bar.add_cascade(label="视图", menu=self.view_menu)

        self.root.config(menu=self.menu_bar)

        # 创建文本显示区域
        self.text_area = tk.Text(self.root, wrap=tk.WORD, font=(self.font_family, self.font_size),
                                 bg=self.bg_color, fg=self.text_color, spacing3=self.line_spacing)
        self.text_area.pack(expand=True, fill='both')

        # 创建导航按钮
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.W)

        self.prev_button = tk.Button(self.button_frame, text="上一页", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.button_frame, text="下一页", command=self.next_page)
        self.next_button.pack(side=tk.LEFT)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.split_pages(content)
                self.show_page()
            except Exception as e:
                messagebox.showerror("错误", f"打开文件失败: {str(e)}")

    def split_pages(self, content):
        self.pages = []
        chars_per_page = 1000  # 每页显示的字符数
        for i in range(0, len(content), chars_per_page):
            self.pages.append(content[i:i + chars_per_page])
        self.current_page = 0

    def show_page(self):
        if self.pages:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.pages[self.current_page])
            self.root.title(f"本地 TXT 小说阅读器 - 第 {self.current_page + 1} 页 / 共 {len(self.pages)} 页")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page()

    def change_font_size(self):
        new_size = simpledialog.askinteger("调整字体大小", "请输入新的字体大小:", initialvalue=self.font_size)
        if new_size:
            self.font_size = new_size
            self.text_area.config(font=(self.font_family, self.font_size))

    def change_font_family(self):
        new_family = simpledialog.askstring("选择字体", "请输入字体名称:", initialvalue=self.font_family)
        if new_family:
            self.font_family = new_family
            self.text_area.config(font=(self.font_family, self.font_size))

    def change_bg_color(self):
        color = colorchooser.askcolor(title="选择背景颜色", initialcolor=self.bg_color)
        if color[1]:
            self.bg_color = color[1]
            self.text_area.config(bg=self.bg_color)

    def change_text_color(self):
        color = colorchooser.askcolor(title="选择文字颜色", initialcolor=self.text_color)
        if color[1]:
            self.text_color = color[1]
            self.text_area.config(fg=self.text_color)

    # 新增调整字体间距方法
    def change_line_spacing(self):
        new_spacing = simpledialog.askinteger("调整字体间距", "请输入新的字体间距（像素）:", initialvalue=self.line_spacing)
        if new_spacing is not None:
            self.line_spacing = new_spacing
            self.text_area.config(spacing3=self.line_spacing)


if __name__ == "__main__":
    root = tk.Tk()
    app = NovelReader(root)
    root.mainloop()
