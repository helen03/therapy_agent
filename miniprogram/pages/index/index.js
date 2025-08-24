// miniprogram/pages/index/index.js
const app = getApp()

Page({
  data: {
    hasLogin: false,
    userInfo: {}
  },

  onLoad() {
    this.checkLoginStatus()
  },

  checkLoginStatus() {
    const hasLogin = app.globalData.hasLogin
    this.setData({ hasLogin })
    
    if (hasLogin) {
      const userInfo = wx.getStorageSync('userInfo')
      this.setData({ userInfo })
    }
  },

  onGetUserInfo(e) {
    const userInfo = e.detail.userInfo
    if (userInfo) {
      this.login(userInfo)
    }
  },

  login(userInfo) {
    wx.showLoading({ title: '登录中...' })
    
    app.login(userInfo)
      .then(res => {
        wx.setStorageSync('token', res.token)
        wx.setStorageSync('userInfo', userInfo)
        app.globalData.hasLogin = true
        app.globalData.userInfo = userInfo
        
        this.setData({ 
          hasLogin: true, 
          userInfo: userInfo 
        })
        
        wx.showToast({ title: '登录成功', icon: 'success' })
        
        // 跳转到聊天页面
        setTimeout(() => {
          wx.switchTab({ url: '/pages/chat/chat' })
        }, 1500)
      })
      .catch(err => {
        console.error('登录失败:', err)
        wx.showToast({ title: '登录失败', icon: 'none' })
      })
      .finally(() => {
        wx.hideLoading()
      })
  },

  navigateToChat() {
    wx.switchTab({ url: '/pages/chat/chat' })
  }
})