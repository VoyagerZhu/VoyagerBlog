'我的主页'
import streamlit as st
import requests
import time 
import os 
import re

st.header("欢迎来到我的主页！")
#功能区
def page_1():
    st.subheader("每日一句")
    url = "https://open.iciba.com/dsapi/"
    r = requests.get(url)
    dic = eval(r.content)
    sentence_eng = dic["content"]
    sentence_ch = dic["note"]
    bg_img = dic["picture2"]
    st.image(bg_img)
    st.subheader(sentence_eng)
    st.subheader(sentence_ch)
    
        
def page_2():
    tab1,tab2 = st.tabs(['阅读博客','发布博客'])
    blog_titles_list = []
    blog_contents_list = []
    blog_upload_time_list = []
    bloggers = []
    with tab2:
        files = os.listdir('./blogs')
        for file in files:
            address = "blogs\{}".format(file)
            with open(address,"r",encoding='utf-8')as f:
                blog_list = f.read().split("\n")
                blog_title = blog_list[0]
                blog_titles_list.append(blog_title)
                blog_upload_time = blog_list[-2]
                blog_upload_time_list.append(blog_upload_time)
                blogger = blog_list[-1]
                bloggers.append(blogger)
                blog_contents_list.append(blog_list[1:-2])
        new_blog_title = st.text_input("请编写标题")
        new_blog_content = st.text_area("请编写属于你的blog")
        if st.button("发布"):
            if st.session_state.logged_in == False:
                st.warning("你还没有登录呢！")
            else:
                if new_blog_title in blog_titles_list:
                    st.warning("标题与其他博客重复啦！请重新修改。")
                    new_blog_title = ""
                else:
                    ltime = str(time.time())
                    address = "blogs\{}.txt".format(ltime)
                    strf_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                    with open(address,"w",encoding='utf-8')as f:
                        new_blog = str(new_blog_title)+"\n"+str(new_blog_content)+"\n"+strf_time+"\n"+st.session_state.username
                        f.write(new_blog)
                    st.success("博客已成功发送~")
                    st.balloons()
                        
    with tab1:
        title = st.selectbox("请选择你想要阅读的博客",blog_titles_list)
        st.header(title)
        list_index = blog_titles_list.index(title)
        watching_blog_time = blog_upload_time_list[list_index]
        blogger_name = bloggers[list_index]
        st.caption(watching_blog_time+"             "+blogger_name)
        for para in blog_contents_list[list_index]:
            st.write(para)

def page_3():
    pass

def page_4():
    with open("passwords.txt","r",encoding='utf-8')as f:
        passwords_list = f.read().split("\n")
    for i in range(len(passwords_list)):
        passwords_list[i] = passwords_list[i].split("#")
    passwords_dict = dict(passwords_list)
    with st.form("login_form"):
        st.subheader("登录/注册")
        login_name = st.text_input("请输入网名")
        login_passward = st.text_input("请输入密码",type="password")
        login_button = st.form_submit_button("提交")
        if login_button:
            if st.session_state.username == login_name:
                st.warning("你已经登录啦！")
            else:
                if login_name == "":
                    st.error("请输入网名")
                elif login_passward == "":
                    st.error("请输入密码")
                else:
                    if login_name in passwords_dict:
                        if login_passward == passwords_dict[login_name]:
                            st.success("恭喜你成功登陆！")
                            st.session_state.logged_in = True
                            st.session_state.username= login_name
                            
                        else:
                            st.error("密码错误，请重试")
                    else:
                        st.info("没有你的账户")
                        if_eng = re.findall(r"[A-Za-z]+",login_passward)
                        if_num = re.findall(r"\d+",login_passward)
                        if len(login_passward) < 5 or if_eng == [] or if_num == []:
                            st.error("密码需要5位及以上，并且需包含字母和数字")
                        else:
                            st.success("恭喜你成功注册！欢迎你加入我们！")
                            st.session_state.logged_in = True
                            st.session_state.username= login_name
                            st.balloons()
                            with open("passwords.txt","a",encoding='utf-8')as f:
                                f.write("\n"+login_name+"#"+login_passward)

#运行区
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if st.session_state:
    page = st.sidebar.radio("我的主页",["首页",'博客天地','创始人简介','登录/注册'])
    st.sidebar.write("用户名："+st.session_state.username)
    if page == "博客天地":
        page_2()
    elif page == "创始人简介":
        page_3()
    elif page == "登录/注册":
        page_4()
    else:
        page_1()
else:
    page_4()
    

    

