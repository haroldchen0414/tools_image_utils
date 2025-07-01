# tools_image_utils
便携图像操作脚本

目前有的功能：  
### 1.fix_type  
恢复jpg和png图片的后缀

### 2.detect_and_remove_duplicate  
检测删除重复的图片  
参数1: hand_control  
hand_control为True时，显示重复的图片，按d删除  
hand_control为False时，自动删除重复的图片

### 3.rename  
重命名图片，将视频移到视频文件夹  
参数1：method  
method为0时，将图片文件命名为xyz_1.jpg这种形式（三个随机小写字母）  
method为1时，将图片命名为1.jpg这种形式  
method为2时，将图片命名为00001.jpg这种形式  
参数2：contain_video  
contain_video为True时，将全部视频文件移动到"视频"文件夹下

### 4.modify_label
为文件夹增加或删除[xP_y_V_zMB]信息  
参数1：method  
method为add时，文件夹名字添加[xP_y_V_zMB]信息  
method为delete时，文件夹名字删除[xP_y_V_zMB]信息



