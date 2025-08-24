// miniprogram/app.js
App({
  onLaunch() {
    console.log('Therapy Agent Mini Program launched')
    
    // 检查登录状态
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.hasLogin = true
    }
  },
  
  globalData: {
    hasLogin: false,
    baseUrl: 'https://your-backend-domain.com/api', // 生产环境API地址
    // baseUrl: 'http://localhost:5000/api', // 开发环境API地址
    userInfo: null
  },
  
  // 统一API请求方法
  apiRequest(url, data = {}, method = 'POST') {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.baseUrl + url,
        data: data,
        method: method,
        header: {
          'content-type': 'application/json',
          'Authorization': wx.getStorageSync('token') ? 'Bearer ' + wx.getStorageSync('token') : ''
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            reject(res.data)
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },
  
  // 登录方法
  login(userInfo) {
    return this.apiRequest('/mobile_login', {
      username: userInfo.nickName,
      avatar: userInfo.avatarUrl
    })
  },
  
  // 发送消息
  sendMessage(message, sessionId) {
    return this.apiRequest('/chat', {
      message: message,
      session_id: sessionId,
      user_id: wx.getStorageSync('user_id') || 'mini_user'
    })
  },
  
  // 获取用户洞察
  getUserInsights() {
    return this.apiRequest('/user_insights', {}, 'GET')
  },
  
  // 获取每日卡片
  getDailyCard() {
    return this.apiRequest('/daily_card', {}, 'GET')
  }
})