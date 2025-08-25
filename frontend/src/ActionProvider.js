import axios from 'axios';
// ActionProvider starter code
class ActionProvider {
  constructor(createChatBotMessage, setStateFunc, createClientMessage) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
    this.createClientMessage = createClientMessage;
  }


  // Asks for password after storing username
  askForPassword = (username) => {
    this.setState((state) => ({
      ...state,
      username: username,
    }));
    const messages = this.createChatBotMessage(
      "Please enter your password:",
      {
        withAvatar: true,
      }
    );

    this.addMessageToBotState(messages);
  }

  // Checking for ID with a request
  updateUserID = async (username, password) => {

    this.setState((state) => ({
      ...state,
      password: password,
    }));

      // Get API base URL from environment or use default for local development
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5001';
    const uri = `${apiBaseUrl}/api/login`
    let user_info = {
      username: username,
      password: password
    };

    const response = await axios.post(uri, {
      user_info
    })

    // dataReceived format: {validID : bool, userID: string}
    let dataReceived = response.data
    if (!dataReceived.validID) {
      let message = this.createChatBotMessage(
        "The ID and password combination is not valid, sorry. What is your user ID?",
        {
          withAvatar: true,
        });
      this.addMessageToBotState(message);
      // let user_id_message = this.createChatBotMessage("What is your user ID?",
      //   { withAvatar: true,
      //     delay: 1500 }
      // );
      // this.addMessageToBotState(user_id_message)
      this.setState((state) => ({
        ...state,
        username: null,
        password: null
      }));

    } else {
      let model_prompt = dataReceived.model_prompt
      this.setState((state) => ({ ...state, userState: dataReceived.userID, inputType: dataReceived.choices, sessionID: dataReceived.sessionID }));
      let message = this.createChatBotMessage("The user ID and password combination is valid, thank you!", {
        withAvatar: true,
      });

      // Opening prompt -> open text
      this.addMessageToBotState(message);
      message = this.createChatBotMessage(model_prompt, {
        withAvatar: true,
        delay: 1500,
      });
      this.addMessageToBotState(message);
    }

  };

  // Send API request
  sendRequest = async (choice_info) => {
    try {
      // Get API base URL from environment or use default for local development
      const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
      const uri = `${apiBaseUrl}/api/update_session`;
      
      console.log("Sending request to:", uri);
      console.log("Request data:", choice_info);
      
      const response = await axios.post(uri, {
        choice_info
      });

      console.log("Received response:", response.data);
      
      // Check if response is valid
      if (response && response.data) {
        this.handleReceivedData(response.data);
      } else {
        // Handle empty or invalid response
        const errorMessage = this.createChatBotMessage(
          "抱歉，我暂时无法处理您的请求。请稍后再试。",
          { withAvatar: true }
        );
        this.addMessageToBotState(errorMessage);
      }
    } catch (error) {
      console.error("API request failed:", error);
      
      // 提供友好的错误消息给用户
      const errorMessage = this.createChatBotMessage(
        "抱歉，我暂时无法处理您的请求。请稍后再试。",
        { withAvatar: true }
      );
      this.addMessageToBotState(errorMessage);
    }
  };

  handleReceivedData = (dataReceived) => {
    try {
      // Validate data received
      if (!dataReceived) {
        console.error("No data received from backend");
        const errorMessage = this.createChatBotMessage(
          "抱歉，我没有收到有效的响应。请稍后再试。",
          { withAvatar: true }
        );
        this.addMessageToBotState(errorMessage);
        return;
      }

      // Extract response and options with fallbacks
      const chatbotResponse = dataReceived.chatbot_response || dataReceived.response || "感谢您的消息。我在这里支持您。";
      const userOptions = dataReceived.user_options || dataReceived.options || ["继续对话", "换个话题", "需要帮助"];
      
      console.log("Processing response:", { chatbotResponse, userOptions });

      let optionsToShow = null;

      // Handle different option types
      if (Array.isArray(userOptions)) {
        // Required options: null or "YesNo" or "Continue" or "Feedback" or "Emotion"}
        if (userOptions.length === 1 && (userOptions[0] === "open_text" || userOptions[0] === "any")) {
          optionsToShow = null;
        } else if (userOptions.length === 1 && userOptions[0] === "continue") {
          optionsToShow = "Continue";
        } else if (userOptions.length === 2 && userOptions[0] === "yes" && userOptions[1] === "no") {
          optionsToShow = "YesNo";
        } else if (userOptions.length === 2 && userOptions[0] === "yes, i would like to try one of these protocols" && userOptions[1] === "no, i would like to try something else") {
          optionsToShow = "YesNoProtocols";
        } else if (userOptions.length === 2 && userOptions[0] === "recent" && userOptions[1] === "distant") {
          optionsToShow = "RecentDistant";
        } else if (userOptions.length === 3 && userOptions[0] === "positive" && userOptions[1] === "neutral" && userOptions[2] === "negative") {
          optionsToShow = "Emotion";
        } else if (userOptions.length === 3 && userOptions[0] === "better" && userOptions[1] === "worse" && userOptions[2] === "no change") {
          optionsToShow = "Feedback";
        } else {
          // Protocol case or default options
          optionsToShow = "Protocol";
          this.setState((state) => ({
            ...state,
            protocols: userOptions,
            askingForProtocol: true
          }));
        }
      } else {
        // Fallback for non-array options
        optionsToShow = null;
      }

      this.setState((state) => ({
        ...state,
        currentOptionToShow: optionsToShow,
      }));

      // Handle responses - either strings or list of strings
      if (typeof chatbotResponse === "string") {
        const messages = this.createChatBotMessage(chatbotResponse, {
          withAvatar: true,
          widget: optionsToShow,
        });
        this.addMessageToBotState(messages);
      } else if (Array.isArray(chatbotResponse)) {
        for (let i = 0; i < chatbotResponse.length; i++) {
          let widget = null;
          // Shows options after last message
          if (i === chatbotResponse.length - 1) {
            widget = optionsToShow;
          }
          const message_to_add = this.createChatBotMessage(chatbotResponse[i], {
            withAvatar: true,
            widget: widget,
            delay: (i)*1500,
          });
          this.addMessageToBotState(message_to_add);
        }
      } else {
        // Fallback for unexpected response format
        const fallbackMessage = this.createChatBotMessage(
          "感谢您的消息。我在这里支持您。请告诉我更多关于您的感受。",
          { withAvatar: true, widget: optionsToShow }
        );
        this.addMessageToBotState(fallbackMessage);
      }
    } catch (error) {
      console.error("Error handling received data:", error);
      const errorMessage = this.createChatBotMessage(
        "抱歉，处理您的消息时出现了问题。请稍后再试。",
        { withAvatar: true }
      );
      this.addMessageToBotState(errorMessage);
    }
  };

  handleButtonsEmotion = (userID, sessionID, userInput, userInputType) => {
    let inputToSend = userInput;
    let message = this.createClientMessage(userInput);
    this.addMessageToBotState(message);


    // Ignores input type above and manually defines; other cases will need an if check for this
    let input_type = ["positive", "neutral", "negative"]
    const dataToSend = {
      user_id: userID,
      session_id: sessionID,
      user_choice: inputToSend,
      input_type: input_type,
    };
    this.sendRequest(dataToSend);
  }

  handleButtons = (userID, sessionID, userInput, userInputType) => {
    let message = this.createClientMessage(userInput);
    this.addMessageToBotState(message);

    const dataToSend = {
      user_id: userID,
      session_id: sessionID,
      user_choice: userInput,
      input_type: userInputType,
    };
    return this.sendRequest(dataToSend);
  };

  askForProtocol = () => {
    let message = "Please type a protocol number (1-20), using the workshops to help you."
    this.addMessageToBotState(message);
    this.setState((state) => ({
      ...state,
      askingForProtocol: true,
    }))
  }

  stopAskingForProtocol = () => {
    this.setState((state) => ({
      ...state,
      askingForProtocol: false,
    }))
  }


  // Copies last message from model - kept for backward compatibility but should use handleInvalidInput instead
  copyLastMessage = () => {
    this.setState((state) => ({
      ...state,
      messages: [...state.messages, state.messages[state.messages.length - 2]],
    }))
  }
  
  // Handles invalid user input by providing helpful feedback
  handleInvalidInput = (expectedOption) => {
    let feedbackMessage = "感谢您的消息。我在这里倾听和支持您，请继续分享您的感受和想法。";
    
    // 在自由文本模式下提供通用的鼓励性反馈
    const message = this.createChatBotMessage(feedbackMessage, {
      withAvatar: true,
    });
    
    this.addMessageToBotState(message);
  }


  // Add message to state
  addMessageToBotState = (message) => {
    this.setState((state) => ({
      ...state,
      messages: [...state.messages, message],
    }));
  };
}

export default ActionProvider;
