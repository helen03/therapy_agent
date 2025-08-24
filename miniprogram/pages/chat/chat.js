// miniprogram/pages/chat/chat.js
const app = getApp()

Page({
  data: {
    messages: [],
    inputValue: '',
    sessionId: '',
    isLoading: false
  },

  onLoad() {
    this.initSession()
    this.addMessage('您好！我是您的治疗助手，随时为您提供支持。', false)
  },

  initSession() {
    let sessionId = wx.getStorageSync('session_id')
    if (!sessionId) {
      sessionId = 'mini_' + Date.now() + '_' + Math.random().toString(36).substr(2)
      wx.setStorageSync('session_id', sessionId)
    }
    this.setData({ sessionId })
  },

  onInput(e) {
    this.setData({ inputValue: e.detail.value })
  },

  sendMessage() {
    const message = this.data.inputValue.trim()
    if (!message) return

    this.setData({ inputValue: '', isLoading: true })
    this.addMessage(message, true)

    app.sendMessage(message, this.data.sessionId)
      .then(res => {
        this.addMessage(res.response, false)
      })
      .catch(err => {
        console.error('发送消息失败:', err)
        this.addMessage('抱歉，暂时无法连接到服务。', false)
      })
      .finally(() => {
        this.setData({ isLoading: false })
      })
  },

  addMessage(text, isUser) {
    const newMessage = {
      id: Date.now(),
      text: text,
      isUser: isUser,
      time: new Date().toLocaleTimeString()
    }

    this.setData({
      messages: [...this.data.messages, newMessage]
    })

    // 滚动到底部
    setTimeout(() => {
      wx.pageScrollTo({
        scrollTop: 9999,
        duration: 300
      })
    }, 100)
  },

  onPullDownRefresh() {
    wx.stopPullDownRefresh()
  }
})