import React, { useState } from 'react';
import { 
  MessageCircle, 
  Upload, 
  Mic, 
  Volume2, 
  Search, 
  Brain, 
  Settings, 
  Smartphone, 
  Monitor, 
  Globe,
  Database,
  Zap,
  FileText,
  Heart,
  Bot,
  Send,
  Play,
  Pause,
  Download,
  User,
  LogIn,
  LogOut,
  Plus,
  History,
  UserPlus,
  Eye,
  EyeOff,
  Mail,
  Lock,
  ArrowLeft,
  Trash2,
  Edit3,
  Clock
} from 'lucide-react';

const AICompanionAssistant = () => {
  const [currentView, setCurrentView] = useState('login');
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('chat');
  const [showPassword, setShowPassword] = useState(false);
  const [activeSessionId, setActiveSessionId] = useState(1);
  
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ 
    username: '', 
    email: '', 
    password: '', 
    confirmPassword: '' 
  });
  
  const [sessions, setSessions] = useState([
    {
      id: 1,
      title: '心理咨询对话',
      lastMessage: '我最近感到有些焦虑...',
      timestamp: '2024-08-25 10:30',
      messageCount: 15,
      isActive: true
    },
    {
      id: 2,
      title: '学习规划讨论',
      lastMessage: '请帮我制定一个学习计划',
      timestamp: '2024-08-24 15:22',
      messageCount: 8,
      isActive: false
    },
    {
      id: 3,
      title: '技术问题咨询',
      lastMessage: 'RAG技术的原理是什么？',
      timestamp: '2024-08-23 09:15',
      messageCount: 23,
      isActive: false
    }
  ]);
  
  const [messages, setMessages] = useState({
    1: [
      { id: 1, type: 'assistant', content: '你好！我是你的AI陪伴助手。我可以帮你处理文档、进行语音交流、提供情感支持。有什么我可以帮助你的吗？', timestamp: '10:30' },
      { id: 2, type: 'user', content: '我最近感到有些焦虑，不知道该怎么办...', timestamp: '10:32' },
      { id: 3, type: 'assistant', content: '我理解你的感受。焦虑是很常见的情绪反应。让我们用CBT的方法来分析一下：\n\n1. 首先识别引发焦虑的具体想法\n2. 评估这些想法的合理性\n3. 寻找更平衡的思维方式\n\n你能告诉我具体是什么让你感到焦虑吗？', timestamp: '10:33' }
    ],
    2: [
      { id: 1, type: 'assistant', content: '你好！我来帮你制定学习计划。', timestamp: '15:22' }
    ],
    3: [
      { id: 1, type: 'assistant', content: 'RAG技术很有趣，让我为你详细解释...', timestamp: '09:15' }
    ]
  });

  const [inputMessage, setInputMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [ragResults, setRagResults] = useState([]);
  const [systemStatus] = useState({
    llm: 'online',
    rag: 'active',
    tts: 'ready',
    mcp: 'connected'
  });

  const handleLogin = (e) => {
    e.preventDefault();
    if (loginForm.email && loginForm.password) {
      setUser({
        id: 1,
        username: 'AI用户',
        email: loginForm.email,
        avatar: null,
        joinDate: '2024-08-01',
        totalSessions: 12,
        totalMessages: 156
      });
      setCurrentView('main');
      setActiveTab('chat');
    }
  };

  const handleRegister = (e) => {
    e.preventDefault();
    if (registerForm.username && registerForm.email && 
        registerForm.password && registerForm.password === registerForm.confirmPassword) {
      setUser({
        id: 1,
        username: registerForm.username,
        email: registerForm.email,
        avatar: null,
        joinDate: new Date().toISOString().split('T')[0],
        totalSessions: 0,
        totalMessages: 0
      });
      setCurrentView('main');
      setActiveTab('chat');
    }
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentView('login');
    setActiveTab('chat');
  };

  const createNewSession = () => {
    const newSession = {
      id: Date.now(),
      title: `新对话 ${sessions.length + 1}`,
      lastMessage: '',
      timestamp: new Date().toLocaleString('zh-CN'),
      messageCount: 0,
      isActive: true
    };
    
    setSessions(prev => [
      newSession,
      ...prev.map(s => ({ ...s, isActive: false }))
    ]);
    setActiveSessionId(newSession.id);
    setMessages(prev => ({ ...prev, [newSession.id]: [] }));
  };

  const switchSession = (sessionId) => {
    setSessions(prev => 
      prev.map(s => ({ 
        ...s, 
        isActive: s.id === sessionId 
      }))
    );
    setActiveSessionId(sessionId);
  };

  const deleteSession = (sessionId) => {
    if (sessions.length <= 1) return;
    
    setSessions(prev => prev.filter(s => s.id !== sessionId));
    setMessages(prev => {
      const newMessages = { ...prev };
      delete newMessages[sessionId];
      return newMessages;
    });
    
    if (activeSessionId === sessionId) {
      const remainingSession = sessions.find(s => s.id !== sessionId);
      if (remainingSession) {
        setActiveSessionId(remainingSession.id);
        switchSession(remainingSession.id);
      }
    }
  };

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      const currentMessages = messages[activeSessionId] || [];
      const newMessage = {
        id: currentMessages.length + 1,
        type: 'user',
        content: inputMessage,
        timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages(prev => ({
        ...prev,
        [activeSessionId]: [...(prev[activeSessionId] || []), newMessage]
      }));
      
      setSessions(prev => 
        prev.map(s => 
          s.id === activeSessionId 
            ? { 
                ...s, 
                lastMessage: inputMessage.length > 30 ? inputMessage.substring(0, 30) + '...' : inputMessage,
                timestamp: new Date().toLocaleString('zh-CN'),
                messageCount: s.messageCount + 1
              }
            : s
        )
      );
      
      setTimeout(() => {
        const aiReply = {
          id: currentMessages.length + 2,
          type: 'assistant',
          content: `我理解你的问题："${inputMessage}"。让我运用CoT思维链来分析：\n\n1. 首先，我会检索相关的知识库信息\n2. 然后结合CBT认知疗法原理\n3. 最后提供个性化的建议\n\n基于RAG检索到的信息，我建议...`,
          timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        };
        
        setMessages(prev => ({
          ...prev,
          [activeSessionId]: [...(prev[activeSessionId] || []), newMessage, aiReply]
        }));
        
        setSessions(prev => 
          prev.map(s => 
            s.id === activeSessionId 
              ? { ...s, messageCount: s.messageCount + 1 }
              : s
          )
        );
      }, 1500);
      
      setInputMessage('');
    }
  };

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    const newFiles = files.map(file => ({
      id: Date.now() + Math.random(),
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'processing'
    }));
    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    setTimeout(() => {
      setUploadedFiles(prev => 
        prev.map(file => 
          newFiles.some(nf => nf.id === file.id) 
            ? { ...file, status: 'vectorized', chunks: Math.floor(file.size / 1000) + 1 }
            : file
        )
      );
    }, 2000);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      setTimeout(() => {
        setIsRecording(false);
        const currentMessages = messages[activeSessionId] || [];
        const voiceMessage = {
          id: currentMessages.length + 1,
          type: 'user',
          content: '语音转文字：我想了解一下CBT认知行为疗法的相关内容',
          isVoice: true,
          timestamp: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        };
        
        setMessages(prev => ({
          ...prev,
          [activeSessionId]: [...(prev[activeSessionId] || []), voiceMessage]
        }));
        
        setSessions(prev => 
          prev.map(s => 
            s.id === activeSessionId 
              ? { 
                  ...s, 
                  lastMessage: '语音消息',
                  timestamp: new Date().toLocaleString('zh-CN'),
                  messageCount: s.messageCount + 1
                }
              : s
          )
        );
      }, 3000);
    }
  };

  if (currentView === 'login') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="w-full max-w-md">
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">AI陪伴助手</h1>
              <p className="text-white/70">登录开始你的陪伴之旅</p>
            </div>
            
            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  邮箱地址
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm(prev => ({ ...prev, email: e.target.value }))}
                    className="w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请输入邮箱地址"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  密码
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={loginForm.password}
                    onChange={(e) => setLoginForm(prev => ({ ...prev, password: e.target.value }))}
                    className="w-full pl-10 pr-12 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请输入密码"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-white/50 hover:text-white/80"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <button
                type="submit"
                className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-105"
              >
                登录
              </button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-white/70">
                还没有账号？
                <button
                  onClick={() => setCurrentView('register')}
                  className="text-purple-400 hover:text-purple-300 font-medium ml-1"
                >
                  立即注册
                </button>
              </p>
            </div>
            
            <div className="mt-6 pt-6 border-t border-white/20">
              <p className="text-center text-white/60 text-sm">
                Demo账号：demo@example.com / 123456
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentView === 'register') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="w-full max-w-md">
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-2xl">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <UserPlus className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">创建账号</h1>
              <p className="text-white/70">加入AI陪伴助手大家庭</p>
            </div>
            
            <form onSubmit={handleRegister} className="space-y-6">
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  用户名
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type="text"
                    value={registerForm.username}
                    onChange={(e) => setRegisterForm(prev => ({ ...prev, username: e.target.value }))}
                    className="w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请输入用户名"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  邮箱地址
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type="email"
                    value={registerForm.email}
                    onChange={(e) => setRegisterForm(prev => ({ ...prev, email: e.target.value }))}
                    className="w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请输入邮箱地址"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  密码
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={registerForm.password}
                    onChange={(e) => setRegisterForm(prev => ({ ...prev, password: e.target.value }))}
                    className="w-full pl-10 pr-12 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请输入密码"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-white/50 hover:text-white/80"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  确认密码
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 w-5 h-5 text-white/50" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={registerForm.confirmPassword}
                    onChange={(e) => setRegisterForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
                    className="w-full pl-10 pr-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                    placeholder="请再次输入密码"
                    required
                  />
                </div>
                {registerForm.password && registerForm.confirmPassword && 
                 registerForm.password !== registerForm.confirmPassword && (
                  <p className="text-red-400 text-sm mt-1">密码不匹配</p>
                )}
              </div>
              
              <button
                type="submit"
                disabled={!registerForm.username || !registerForm.email || 
                         !registerForm.password || registerForm.password !== registerForm.confirmPassword}
                className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed rounded-lg font-semibold text-white transition-all duration-300 transform hover:scale-105 disabled:hover:scale-100"
              >
                注册
              </button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-white/70">
                已有账号？
                <button
                  onClick={() => setCurrentView('login')}
                  className="text-purple-400 hover:text-purple-300 font-medium ml-1"
                >
                  立即登录
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
      <nav className="bg-black/20 backdrop-blur-md border-b border-white/10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                AI陪伴助手
              </h1>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4">
                {Object.entries(systemStatus).map(([key, status]) => (
                  <div key={key} className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${
                      status === 'online' || status === 'active' || status === 'ready' || status === 'connected' 
                        ? 'bg-green-400' : 'bg-red-400'
                    }`}></div>
                    <span className="text-sm uppercase">{key}</span>
                  </div>
                ))}
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 bg-white/10 rounded-lg px-3 py-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <div className="text-sm">
                    <div className="text-white font-medium">{user?.username}</div>
                    <div className="text-white/60 text-xs">{user?.totalSessions} 会话</div>
                  </div>
                </div>
                
                <button
                  onClick={handleLogout}
                  className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all group"
                  title="登出"
                >
                  <LogOut className="w-5 h-5 text-white/70 group-hover:text-white" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-6">
        <div className="mb-6">
          <div className="flex space-x-1 bg-white/10 rounded-lg p-1 backdrop-blur-sm">
            {[
              { id: 'chat', label: '智能对话', icon: MessageCircle },
              { id: 'sessions', label: '对话历史', icon: History },
              { id: 'architecture', label: '系统架构', icon: Settings },
              { id: 'rag', label: 'RAG检索', icon: Search },
              { id: 'platforms', label: '多平台', icon: Smartphone }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all ${
                  activeTab === tab.id 
                    ? 'bg-white/20 text-white shadow-lg' 
                    : 'text-white/70 hover:text-white hover:bg-white/10'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'chat' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[600px]">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 flex flex-col">
              <div className="p-4 border-b border-white/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">对话会话</h3>
                  <button
                    onClick={createNewSession}
                    className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg transition-all"
                    title="新建对话"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto p-2 space-y-2">
                {sessions.map(session => (
                  <div
                    key={session.id}
                    onClick={() => switchSession(session.id)}
                    className={`p-3 rounded-lg cursor-pointer transition-all group ${
                      session.isActive 
                        ? 'bg-white/20 border border-purple-400/50' 
                        : 'bg-white/10 hover:bg-white/15'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-medium text-sm truncate flex-1 mr-2">
                        {session.title}
                      </h4>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteSession(session.id);
                        }}
                        className="opacity-0 group-hover:opacity-100 p-1 text-red-400 hover:text-red-300 transition-all"
                        title="删除会话"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </div>
                    <p className="text-xs text-white/60 truncate mb-1">
                      {session.lastMessage || '暂无消息'}
                    </p>
                    <div className="flex items-center justify-between text-xs text-white/50">
                      <span className="flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {session.timestamp.split(' ')[1]}
                      </span>
                      <span>{session.messageCount} 条消息</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="lg:col-span-2 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 flex flex-col">
              <div className="p-4 border-b border-white/20">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold flex items-center">
                    <Bot className="w-5 h-5 mr-2" />
                    {sessions.find(s => s.id === activeSessionId)?.title || '智能对话'}
                  </h3>
                  <button
                    className="p-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
                    title="编辑标题"
                  >
                    <Edit3 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {(messages[activeSessionId] || []).length === 0 ? (
                  <div className="text-center py-8 text-white/50">
                    <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>开始新的对话吧！</p>
                  </div>
                ) : (
                  (messages[activeSessionId] || []).map(message => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] p-4 rounded-lg ${
                          message.type === 'user'
                            ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                            : 'bg-white/20 text-white border border-white/30'
                        }`}
                      >
                        {message.isVoice && (
                          <div className="flex items-center mb-2 text-sm opacity-75">
                            <Mic className="w-4 h-4 mr-1" />
                            语音消息
                          </div>
                        )}
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        <div className="text-xs opacity-75 mt-2">{message.timestamp}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
              
              <div className="p-4 border-t border-white/20">
                <div className="flex items-center space-x-2">
                  <input
                    type="file"
                    multiple
                    onChange={handleFileUpload}
                    className="hidden"
                    id="file-upload"
                    accept=".pdf,.doc,.docx,.txt,.md"
                  />
                  <label
                    htmlFor="file-upload"
                    className="p-2 bg-white/20 hover:bg-white/30 rounded-lg cursor-pointer transition-all"
                  >
                    <Upload className="w-5 h-5" />
                  </label>
                  
                  <button
                    onClick={toggleRecording}
                    className={`p-2 rounded-lg transition-all ${
                      isRecording ? 'bg-red-500 animate-pulse' : 'bg-white/20 hover:bg-white/30'
                    }`}
                  >
                    <Mic className="w-5 h-5" />
                  </button>
                  
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="输入消息或上传文档..."
                    className="flex-1 px-4 py-2 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50"
                  />
                  
                  <button
                    onClick={handleSendMessage}
                    className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg transition-all"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                
                {isRecording && (
                  <div className="mt-2 text-center text-sm text-purple-300 animate-pulse">
                    正在录音... 点击麦克风停止
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <h4 className="font-semibold mb-3 flex items-center">
                  <Volume2 className="w-4 h-4 mr-2" />
                  语音合成
                </h4>
                <div className="space-y-2">
                  <button
                    onClick={() => setIsPlaying(!isPlaying)}
                    className="w-full flex items-center justify-center space-x-2 py-2 bg-purple-500/20 hover:bg-purple-500/30 rounded-lg transition-all"
                  >
                    {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    <span>{isPlaying ? '暂停播放' : '播放最后回复'}</span>
                  </button>
                  
                  <div className="text-sm text-white/70">
                    音色: 温暖女声 | 语速: 正常
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <h4 className="font-semibold mb-3 flex items-center">
                  <Heart className="w-4 h-4 mr-2" />
                  CBT情绪分析
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>情绪状态</span>
                    <span className="text-green-300">平静</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>压力指数</span>
                    <span className="text-yellow-300">中等</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>建议</span>
                    <span className="text-blue-300">深呼吸</span>
                  </div>
                </div>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <h4 className="font-semibold mb-3 flex items-center">
                  <Settings className="w-4 h-4 mr-2" />
                  MCP工具
                </h4>
                <div className="space-y-2 text-sm">
                  {['日历查询', '天气预报', '文件处理', '计算器'].map(tool => (
                    <div key={tool} className="flex items-center justify-between">
                      <span>{tool}</span>
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sessions' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[
                { label: '总会话数', value: user?.totalSessions, icon: MessageCircle, color: 'from-blue-500 to-purple-500' },
                { label: '总消息数', value: user?.totalMessages, icon: Bot, color: 'from-purple-500 to-pink-500' },
                { label: '今日对话', value: 3, icon: Clock, color: 'from-green-500 to-blue-500' },
                { label: '平均满意度', value: '4.8/5.0', icon: Heart, color: 'from-pink-500 to-red-500' }
              ].map((stat, index) => (
                <div key={index} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold text-white">{stat.value}</div>
                      <div className="text-white/70 text-sm">{stat.label}</div>
                    </div>
                    <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-full flex items-center justify-center`}>
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
              <div className="p-6 border-b border-white/20">
                <h3 className="text-xl font-semibold flex items-center">
                  <History className="w-5 h-5 mr-2" />
                  对话历史记录
                </h3>
              </div>
              
              <div className="p-6 space-y-4 max-h-96 overflow-y-auto">
                {sessions.map(session => (
                  <div
                    key={session.id}
                    className="bg-white/10 rounded-lg p-4 border border-white/20 hover:bg-white/15 transition-all cursor-pointer"
                    onClick={() => {
                      switchSession(session.id);
                      setActiveTab('chat');
                    }}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-lg text-white">{session.title}</h4>
                      <div className="flex items-center space-x-3">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          session.isActive ? 'bg-green-500/20 text-green-300' : 'bg-gray-500/20 text-gray-300'
                        }`}>
                          {session.isActive ? '当前会话' : '历史会话'}
                        </span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteSession(session.id);
                          }}
                          className="p-1 text-red-400 hover:text-red-300 hover:bg-red-500/20 rounded transition-all"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
                      <div className="flex items-center space-x-2 text-sm text-white/70">
                        <MessageCircle className="w-4 h-4" />
                        <span>{session.messageCount} 条消息</span>
                      </div>
                      <div className="flex items-center space-x-2 text-sm text-white/70">
                        <Clock className="w-4 h-4" />
                        <span>{session.timestamp}</span>
                      </div>
                      <div className="flex items-center space-x-2 text-sm text-white/70">
                        <Bot className="w-4 h-4" />
                        <span>AI陪伴</span>
                      </div>
                    </div>
                    
                    {session.lastMessage && (
                      <div className="bg-white/10 rounded p-3">
                        <div className="text-sm text-white/60 mb-1">最后消息：</div>
                        <div className="text-white/90 text-sm">{session.lastMessage}</div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'architecture' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Monitor className="w-5 h-5 mr-2" />
                前端架构
              </h3>
              <div className="space-y-3">
                {[
                  { name: 'Web界面', tech: 'React + TypeScript', status: 'active' },
                  { name: '微信小程序', tech: 'uni-app', status: 'active' },
                  { name: 'Android应用', tech: 'Flutter', status: 'active' },
                  { name: 'iOS应用', tech: 'Flutter', status: 'development' }
                ].map(item => (
                  <div key={item.name} className="flex items-center justify-between p-3 bg-white/10 rounded-lg">
                    <div>
                      <div className="font-medium">{item.name}</div>
                      <div className="text-sm text-white/70">{item.tech}</div>
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs ${
                      item.status === 'active' ? 'bg-green-500/20 text-green-300' : 'bg-yellow-500/20 text-yellow-300'
                    }`}>
                      {item.status === 'active' ? '运行中' : '开发中'}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Database className="w-5 h-5 mr-2" />
                后端服务
              </h3>
              <div className="space-y-3">
                {[
                  { name: 'API网关', tech: 'Node.js + Express', load: '85%' },
                  { name: '大模型服务', tech: 'Python + FastAPI', load: '60%' },
                  { name: '向量数据库', tech: 'Pinecone/Weaviate', load: '45%' },
                  { name: 'MCP协议', tech: 'WebSocket', load: '30%' }
                ].map(item => (
                  <div key={item.name} className="p-3 bg-white/10 rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <div className="font-medium">{item.name}</div>
                      <div className="text-sm text-white/70">{item.load}</div>
                    </div>
                    <div className="text-sm text-white/70 mb-2">{item.tech}</div>
                    <div className="w-full bg-white/20 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-purple-400 to-pink-400 h-2 rounded-full transition-all duration-300"
                        style={{ width: item.load }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Brain className="w-5 h-5 mr-2" />
                核心功能
              </h3>
              <div className="space-y-4">
                {[
                  { name: 'CoT思维链', desc: '逐步推理分析', icon: Zap },
                  { name: 'RAG检索', desc: '知识库增强生成', icon: Search },
                  { name: 'CBT疗法', desc: '认知行为治疗', icon: Heart },
                  { name: 'TTS语音', desc: '文字转语音输出', icon: Volume2 },
                  { name: '工具调用', desc: 'MCP协议工具集成', icon: Settings }
                ].map(feature => (
                  <div key={feature.name} className="flex items-start space-x-3 p-3 bg-white/10 rounded-lg hover:bg-white/20 transition-all">
                    <feature.icon className="w-5 h-5 mt-0.5 text-purple-400" />
                    <div>
                      <div className="font-medium">{feature.name}</div>
                      <div className="text-sm text-white/70">{feature.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'rag' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <FileText className="w-5 h-5 mr-2" />
                文档向量化
              </h3>
              
              <div className="mb-4">
                <input
                  type="file"
                  multiple
                  onChange={handleFileUpload}
                  className="hidden"
                  id="rag-file-upload"
                  accept=".pdf,.doc,.docx,.txt,.md"
                />
                <label
                  htmlFor="rag-file-upload"
                  className="w-full flex items-center justify-center space-x-2 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg cursor-pointer transition-all"
                >
                  <Upload className="w-5 h-5" />
                  <span>上传文档进行向量化</span>
                </label>
              </div>

              <div className="space-y-3 max-h-80 overflow-y-auto">
                {uploadedFiles.map(file => (
                  <div key={file.id} className="p-3 bg-white/10 rounded-lg border border-white/30">
                    <div className="flex justify-between items-start mb-2">
                      <div className="font-medium truncate">{file.name}</div>
                      <div className={`px-2 py-1 rounded-full text-xs ${
                        file.status === 'processing' ? 'bg-yellow-500/20 text-yellow-300' :
                        file.status === 'vectorized' ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'
                      }`}>
                        {file.status === 'processing' ? '处理中' : 
                         file.status === 'vectorized' ? '已向量化' : '失败'}
                      </div>
                    </div>
                    <div className="text-sm text-white/70">
                      大小: {Math.round(file.size / 1024)}KB
                      {file.chunks && ` | 分块: ${file.chunks}个`}
                    </div>
                    {file.status === 'processing' && (
                      <div className="mt-2 w-full bg-white/20 rounded-full h-1">
                        <div className="bg-gradient-to-r from-yellow-400 to-orange-400 h-1 rounded-full animate-pulse w-1/2"></div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Search className="w-5 h-5 mr-2" />
                智能检索
              </h3>
              
              <div className="mb-4">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="输入问题进行RAG检索..."
                    className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder-white/50 pr-12"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && e.target.value) {
                        setRagResults([
                          { id: 1, source: '用户手册.pdf', content: '根据文档内容，AI陪伴助手支持多种对话模式...', similarity: 0.95 },
                          { id: 2, source: 'CBT指南.docx', content: 'CBT认知行为疗法的核心原理是改变负面思维模式...', similarity: 0.87 },
                          { id: 3, source: '技术文档.md', content: 'RAG系统使用向量数据库存储和检索相关信息...', similarity: 0.82 }
                        ]);
                      }
                    }}
                  />
                  <Search className="absolute right-4 top-3.5 w-5 h-5 text-white/50" />
                </div>
              </div>

              <div className="space-y-3 max-h-96 overflow-y-auto">
                {ragResults.map(result => (
                  <div key={result.id} className="p-4 bg-white/10 rounded-lg border border-white/30">
                    <div className="flex justify-between items-center mb-2">
                      <div className="font-medium text-purple-300">{result.source}</div>
                      <div className="text-sm bg-green-500/20 text-green-300 px-2 py-1 rounded-full">
                        {Math.round(result.similarity * 100)}% 匹配
                      </div>
                    </div>
                    <div className="text-sm text-white/80">{result.content}</div>
                  </div>
                ))}
                
                {ragResults.length === 0 && (
                  <div className="text-center py-8 text-white/50">
                    <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>输入问题开始RAG检索</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'platforms' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                name: 'Web网页版',
                icon: Globe,
                tech: 'React + TypeScript',
                features: ['响应式设计', '实时通信', 'PWA支持'],
                status: 'active',
                users: '15.2K'
              },
              {
                name: '微信小程序',
                icon: MessageCircle,
                tech: 'uni-app',
                features: ['微信登录', '消息推送', '分享功能'],
                status: 'active',
                users: '8.7K'
              },
              {
                name: 'Android应用',
                icon: Smartphone,
                tech: 'Flutter',
                features: ['原生体验', '离线模式', '推送通知'],
                status: 'active',
                users: '12.3K'
              },
              {
                name: 'iOS应用',
                icon: Smartphone,
                tech: 'Flutter',
                features: ['App Store', 'Face ID', 'Siri集成'],
                status: 'development',
                users: 'Soon'
              }
            ].map((platform, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-all">
                <div className="flex items-center justify-between mb-4">
                  <platform.icon className="w-8 h-8 text-purple-400" />
                  <div className={`px-3 py-1 rounded-full text-xs ${
                    platform.status === 'active' 
                      ? 'bg-green-500/20 text-green-300' 
                      : 'bg-yellow-500/20 text-yellow-300'
                  }`}>
                    {platform.status === 'active' ? '已发布' : '开发中'}
                  </div>
                </div>
                
                <h3 className="text-lg font-semibold mb-2">{platform.name}</h3>
                <p className="text-white/70 text-sm mb-4">{platform.tech}</p>
                
                <div className="space-y-2 mb-4">
                  {platform.features.map((feature, fIndex) => (
                    <div key={fIndex} className="flex items-center space-x-2 text-sm">
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full"></div>
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
                
                <div className="flex items-center justify-between pt-4 border-t border-white/20">
                  <span className="text-sm text-white/70">活跃用户</span>
                  <span className="font-semibold text-purple-300">{platform.users}</span>
                </div>
                
                {platform.status === 'active' && (
                  <button className="w-full mt-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-lg transition-all flex items-center justify-center space-x-2">
                    <Download className="w-4 h-4" />
                    <span>立即体验</span>
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <footer className="mt-12 bg-black/20 backdrop-blur-md border-t border-white/10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>系统运行正常</span>
              </div>
              <div>延迟: 127ms</div>
              <div>在线用户: 2,847</div>
              <div className="text-white/50">|</div>
              <div>欢迎回来，{user?.username}</div>
              <div>加入时间: {user?.joinDate}</div>
            </div>
            
            <div className="text-white/70">
              AI陪伴助手 v2.0 | 支持CoT、RAG、CBT、MCP
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AICompanionAssistant;