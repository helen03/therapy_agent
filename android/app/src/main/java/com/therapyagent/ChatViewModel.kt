package com.therapyagent

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.MediaType
import org.json.JSONObject

class ChatViewModel : ViewModel() {
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages

    private val client = OkHttpClient()
    private val baseUrl = "http://10.0.2.2:5000" // 本地开发服务器

    init {
        // 添加欢迎消息
        addMessage("您好！我是您的治疗助手，随时为您提供支持。", false)
    }

    fun sendMessage(text: String) {
        addMessage(text, true)
        
        viewModelScope.launch {
            try {
                val response = sendToBackend(text)
                addMessage(response, false)
            } catch (e: Exception) {
                addMessage("抱歉，暂时无法连接到服务。请检查网络连接。", false)
            }
        }
    }

    private suspend fun sendToBackend(message: String): String {
        val json = JSONObject()
        json.put("message", message)
        json.put("session_id", "android_session")

        val requestBody = RequestBody.create(
            MediaType.parse("application/json"), 
            json.toString()
        )

        val request = Request.Builder()
            .url("$baseUrl/api/chat")
            .post(requestBody)
            .build()

        val response = client.newCall(request).execute()
        val responseBody = response.body()?.string()
        
        return if (response.isSuccessful && responseBody != null) {
            JSONObject(responseBody).getString("response")
        } else {
            "抱歉，服务暂时不可用。"
        }
    }

    private fun addMessage(text: String, isUser: Boolean) {
        val newMessage = ChatMessage(text, isUser)
        _messages.value = _messages.value + newMessage
    }
}

data class ChatMessage(val text: String, val isUser: Boolean)