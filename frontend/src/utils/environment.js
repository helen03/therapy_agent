/**
 * 环境检测工具
 * 用于检测当前运行环境并返回相应的配置
 */

export const getEnvironment = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  const port = window.location.port;

  const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';
  const isDevelopment = process.env.NODE_ENV === 'development';
  const isProduction = process.env.NODE_ENV === 'production';

  // API基础URL
  let apiBaseUrl;
  if (process.env.REACT_APP_API_BASE_URL) {
    apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
  } else if (isLocalhost) {
    apiBaseUrl = 'http://localhost:5001';
  } else {
    // 生产环境使用相对路径或根据域名推断
    apiBaseUrl = port ? `${protocol}//${hostname}:${port}` : `${protocol}//${hostname}`;
    // 如果API端口与前端不同，需要指定端口
    if (!port || port !== '5001') {
      apiBaseUrl = `${protocol}//${hostname}:5001`;
    }
  }

  return {
    hostname,
    protocol,
    port,
    isLocalhost,
    isDevelopment,
    isProduction,
    apiBaseUrl,
    nodeEnv: process.env.NODE_ENV,
    reactEnv: process.env.REACT_APP_ENV,
  };
};

// 调试信息输出
export const logEnvironment = () => {
  const env = getEnvironment();
  console.log('=== Environment Info ===');
  console.log('Hostname:', env.hostname);
  console.log('Protocol:', env.protocol);
  console.log('Port:', env.port);
  console.log('Is Localhost:', env.isLocalhost);
  console.log('Is Development:', env.isDevelopment);
  console.log('Is Production:', env.isProduction);
  console.log('API Base URL:', env.apiBaseUrl);
  console.log('Node Env:', env.nodeEnv);
  console.log('React Env:', env.reactEnv);
  console.log('=======================');
};