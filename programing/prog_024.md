## Rust 学习笔记

参考书：https://kaisery.github.io/trpl-zh-cn/ch03-03-how-functions-work.html


## 0.概述

Rust是编译型语言，rustc是编译器，cargo是项目管理工具。rustup doc可以查看本地文档。

## 1. cargo

cargo换源：https://lug.ustc.edu.cn/wiki/mirrors/help/rust-crates

#### 1.1 Cargo.toml

cargo期望源文件位于src目录。cargo需要一个配置文件`Cargo.toml`，toml即(Tom's Obvious, Minimal Language)，格式类似于ini文件。下面是一个例子：

```
[package]

name = "hello_world"
version = "0.0.1"
authors = ["jczhang <zhjcyx@gmail.com>"]
```

#### 1.2 命令

建好Cargo.toml文件之后，可以用`cargo build`进行程序构建。生成的二进制路径应该是`target/debug/hello_world`。也可以合并这两步直接用`cargo run`编译和执行二进制程序。注意，这样使debug版本，如果要生成release版本，应该用`cargo build --release`,这样二进制路径应该是`target/release/hello_world`。Release编译速度较慢，但程序执行会更快。

Cargo也提供建立“骨架项目”的命令，如：
```
cargo new hello_world
```
这个命令会创建一个`Cargo.toml`和一个包含`main.rs`的`src目录`。`main.rs`已经写好了一行 `println!("Hello, world!");` 代码，并且项目目录被创建好了一个**git仓库**。

`cargo check`可以检查是否可以正确编译而不编译，这样可以比build更快地检查语法错误。


## 2. 杂项

* `//` 表示注释。

* `use` 引入包含的包。

* 缩进用**空格而非tab**。

* 声明一个变量用`let`，如：
```rust
let foo = 0;        // 可变
let mut bar = 1;    // 不可变
let mut guess = String::new() // 创建可变变量，并绑定到新的String空实例上。
```

* 用`println!`进行打印时，占位符是`{}`。其他和C语言`printf`很类似。例：
```rust
println!("x = {} and y = {}", x, y);
```

* crate是rust的库或者二进制，分别称为库crate，或者二进制crate。crate中又包含有trait。 运行 `cargo doc --open` 命令来构建所有本地依赖提供的文档，并在浏览器中打开，这样可以确定包含哪个trait和调用声明方法。
```rust
use rand::Rng // rand是一个库crate，Rng是rand的一个trait
```

## 3. 变量

#### 3.1 可变，不可变和常量

Rust的**变量**分为可变(mutable)和不可变(immutable)变量，默认是不可变的。与不可变量类似的是**常量**(const)，但是常量只能以常量表达式初始化，并且需要指明类型。例：


```rust
let x = 5;                          // 不可变量
let mut y = 6;                      // 可变量   
const MAX_POINTS: u32 = 100_000;    // 常量，注意数字中的下划线是为了可读性
```

#### 3.2 隐藏 (Shadowing)

Rust中变量声明可以重名，先声明的量会被后声明的同名量**隐藏** (Shadowing)。

利用“隐藏”，可以“改变”不可变量的值。这种改变方法，其实比改变可变量更灵活，因为实质上我们可以创建一个同名不同类型的新的不可变量，例如：
```rust
let spaces = "   ";
let spaces = spaces.len();
```

#### 3.3 数据类型

Rust是静态类型语言，即编译时需要确定所有变量的类型。

* 整形：

|长度(bits)|有符号|无符号|
|-|-|-|
|8|i8|u8|
|16|i16|u16|
|32|i32|u32|
|64|i64|u64|
|arch|isize|usize|

(对于isize/usize，若在64位机器上即使64位，否则为32位。)

* 整形字面值：

|数字字面值	|例子|
|-|-|
|Decimal|	98_222|
|Hex	|0xff|
|Octal|	0o77|
|Binary|	0b1111_0000|
|Byte (u8 only)|	b'A'|


* 浮点型：

|长度(bit)|类型|
|-|-|
|32|f32|
|64|f64|

* 布尔型： `bool`，只有两个可能值：`true`和`false`

* 字符型： `char`， Rust中的char并非1个字节，它支持unicode。char字符用单引号包围。如：
```rust
let c = 'z';
let z = '哈';
let heart_eyed_cat = '😻';
```

### 3.4. 复合类型

Rust 复合类型包括tuple和array：

* tuple：

```rust
// 声明tuple：
let foo = (500, 6.4, 1);
let x: (i32, f64, u8) = (500, 6.4, 1);
// 解构tuple:
let (x, y, z) = foo;
// 索引tuple，注意是用“.” 而非广泛使用的中括号
let five_hundred = x.0;
let one = x.2;
```
* Array

```rust
// 声明一个数组
// 注意类型后加分号，再加数字，这里说明a数组包含了5个i32类型的元素
let a: [i32; 5] = [1, 2, 3, 4, 5];
// 数组的索引是用中括号 "[]"
let first = a[0];
```

注意：如果索引超出了数组长度，Rust 会 panic，这是 Rust 术语，它用于程序因为错误而退出的情况。





