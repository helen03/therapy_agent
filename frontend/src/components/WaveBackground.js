import React, { useRef, useEffect } from 'react';

const WaveBackground = () => {
  const waveRef = useRef(null);
  
  useEffect(() => {
    const canvas = waveRef.current;
    const ctx = canvas.getContext('2d');
    
    // 设置画布尺寸
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // 波浪参数
    const waves = [
      {
        y: canvas.height * 0.7,
        length: 0.01,
        amplitude: 30,
        frequency: 0.01,
        color: 'rgba(99, 102, 241, 0.1)',
        speed: 0.02
      },
      {
        y: canvas.height * 0.75,
        length: 0.015,
        amplitude: 25,
        frequency: 0.015,
        color: 'rgba(139, 92, 246, 0.08)',
        speed: 0.025
      },
      {
        y: canvas.height * 0.8,
        length: 0.02,
        amplitude: 20,
        frequency: 0.02,
        color: 'rgba(236, 72, 153, 0.06)',
        speed: 0.03
      }
    ];
    
    let time = 0;
    
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      waves.forEach((wave, index) => {
        ctx.beginPath();
        ctx.moveTo(0, canvas.height);
        
        // 绘制波浪
        for (let x = 0; x <= canvas.width; x += 5) {
          const y = wave.y + Math.sin(x * wave.length + time * wave.speed) * wave.amplitude;
          ctx.lineTo(x, y);
        }
        
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.closePath();
        
        // 创建渐变填充
        const gradient = ctx.createLinearGradient(0, wave.y - wave.amplitude, 0, canvas.height);
        gradient.addColorStop(0, wave.color);
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.fill();
        
        // 添加波浪顶部发光效果
        ctx.beginPath();
        for (let x = 0; x <= canvas.width; x += 5) {
          const y = wave.y + Math.sin(x * wave.length + time * wave.speed) * wave.amplitude;
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.strokeStyle = wave.color.replace('0.1', '0.3').replace('0.08', '0.25').replace('0.06', '0.2');
        ctx.lineWidth = 2;
        ctx.shadowBlur = 10;
        ctx.shadowColor = wave.color;
        ctx.stroke();
      });
      
      time += 1;
      requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);
  
  return (
    <canvas
      ref={waveRef}
      className="wave-background"
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 2,
        pointerEvents: 'none'
      }}
    />
  );
};

export default WaveBackground;