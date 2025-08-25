// MessageParser starter code
class MessageParser {
  constructor(actionProvider, state) {
    this.actionProvider = actionProvider;
    this.state = state;
  }

  // This method is called inside the chatbot when it receives a message from the user.
  parse(message) {
    console.log('MessageParser received:', message);
    console.log('Current state:', this.state);
    
    // Case: User is already logged in, proceed with normal message processing
    if (this.state.userState !== null && this.state.sessionID !== null) {
      console.log('User is logged in, processing message...');
      let input_type = null;
      if (this.state.inputType && this.state.inputType.length === 1) {
        input_type = this.state.inputType[0]
      } else {
        input_type = this.state.inputType || null
      }
      const currentOptionToShow = this.state.currentOptionToShow
      
      // Handle protocol selection case
      if (this.state.askingForProtocol) {
        if (parseInt(message) >= 1 && parseInt(message) <= 20) {
          const choice_info = {
            user_id: this.state.userState,
            session_id: this.state.sessionID,
            user_choice: message,
            input_type: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
          };
          this.actionProvider.stopAskingForProtocol();
          return this.actionProvider.sendRequest(choice_info);
        } else {
          return this.actionProvider.askForProtocol();
        }
      }
      
      // Check if input matches expected options
      // 修改为总是允许自由文本输入，不进行选项验证
      const isValidInput = true;
      
      console.log('Input validation bypassed, allowing free text input');
      
      if (isValidInput) {
        const choice_info = {
          user_id: this.state.userState,
          session_id: this.state.sessionID,
          user_choice: message,
          input_type: input_type,
        };
        console.log('Sending choice_info:', choice_info);
        return this.actionProvider.sendRequest(choice_info);
      } else {
        // 保留处理无效输入的逻辑，但正常情况下不会执行到这里
        console.log('Invalid input, showing feedback');
        this.actionProvider.handleInvalidInput(currentOptionToShow);
      }
    } else {
      console.log('User not logged in, ignoring message');
      console.log('userState:', this.state.userState);
      console.log('sessionID:', this.state.sessionID);
    }
    // No fallback to login/password prompts when user is already logged in via main login page
  }
}

export default MessageParser;
