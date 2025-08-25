// 工具页面内容 - 简化版
const toolPages = {
    '呼吸练习': {
        title: '呼吸练习',
        content: `
            <div style="display: flex; justify-content: center; margin: 2rem 0;">
                <div style="width: 200px; height: 200px; border-radius: 50%; background: linear-gradient(135deg, #6673f6 0%, #55bff7 100%); display: flex; justify-content: center; align-items: center; color: white; font-size: 1.5rem; font-weight: bold; animation: breathe 20s infinite;">
                    <span id="breathing-text">吸气</span>
                </div>
            </div>
            <style>
                @keyframes breathe {
                    0%, 100% { transform: scale(1); }
                    25% { transform: scale(1.2); }
                    50% { transform: scale(1.2); }
                    75% { transform: scale(1); }
                }
            </style>
            <script>
                // 呼吸动画文本控制
                const breathingText = document.getElementById('breathing-text');
                if (breathingText) {
                    setInterval(() => {
                        const now = new Date().getTime();
                        const phase = (now % 20000) / 20000;
                        if (phase < 0.25) {
                            breathingText.textContent = '吸气';
                        } else if (phase < 0.75) {
                            breathingText.textContent = '屏住';
                        } else {
                            breathingText.textContent = '呼气';
                        }
                    }, 100);
                }
            </script>
        `
    },
    '正念冥想': {
        title: '正念冥想',
        content: `
            <h2>正念冥想指南</h2>
            <p>正念冥想有助于提高专注力，减轻压力，增强自我意识。</p>
            <h3>基本正念冥想步骤</h3>
            <ol>
                <li>找一个安静舒适的地方坐下</li>
                <li>保持身体挺直但放松</li>
                <li>将注意力集中在呼吸上</li>
                <li>当思绪飘走时，温柔地将注意力带回呼吸</li>
                <li>从每天5分钟开始，逐渐增加到15-20分钟</li>
            </ol>
        `
    },
    '情绪日记': {
        title: '情绪日记',
        content: `
            <h2>情绪日记</h2>
            <p>记录你的情绪可以帮助你更好地理解和管理它们。</p>
            <div style="display: flex; flex-direction: column; gap: 2rem;">
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <label>日期:</label>
                    <input type="date" id="journal-date">

                    <label>今天的主要情绪:</label>
                    <select id="journal-emotion">
                        <option value="开心">开心</option>
                        <option value="生气">生气</option>
                        <option value="悲伤">悲伤</option>
                        <option value="焦虑">焦虑</option>
                        <option value="平静">平静</option>
                        <option value="其他">其他</option>
                    </select>

                    <label>引发情绪的事件:</label>
                    <textarea rows="3" id="journal-situation"></textarea>

                    <button onclick="saveJournalEntry()" style="background: linear-gradient(135deg, #6673f6 0%, #55bff7 100%); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 25px; cursor: pointer; font-size: 1rem; align-self: flex-start;">保存日记</button>
                </div>
                <div id="journalEntries" style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px;">
                    <h3>过往日记</h3>
                    <!-- 日记条目将动态加载 -->
                </div>
            </div>
            <script>
                // 加载保存的日记
                function loadJournalEntries() {
                    const entries = JSON.parse(localStorage.getItem('emotionJournalEntries') || '[]');
                    const container = document.getElementById('journalEntries');
                    container.innerHTML = '<h3>过往日记</h3>';
                    entries.forEach(entry => {
                        const entryElement = document.createElement('div');
                        entryElement.style.background = 'white';
                        entryElement.style.padding = '1rem';
                        entryElement.style.marginBottom = '1rem';
                        entryElement.style.borderRadius = '8px';
                        entryElement.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                        entryElement.innerHTML = `
                            <div style="font-weight: bold; color: #6673f6;">${entry.date}</div>
                            <div><strong>情绪:</strong> ${entry.emotion}</div>
                            <div><strong>事件:</strong> ${entry.situation}</div>
                        `;
                        container.appendChild(entryElement);
                    });
                }

                // 保存日记条目
                function saveJournalEntry() {
                    const date = document.getElementById('journal-date').value;
                    const emotion = document.getElementById('journal-emotion').value;
                    const situation = document.getElementById('journal-situation').value;

                    if (!date || !emotion || !situation) {
                        alert('请填写日期、情绪和引发事件');
                        return;
                    }

                    const entry = {
                        date, emotion, situation
                    };

                    const entries = JSON.parse(localStorage.getItem('emotionJournalEntries') || '[]');
                    entries.unshift(entry);
                    localStorage.setItem('emotionJournalEntries', JSON.stringify(entries));

                    // 清空表单
                    document.getElementById('journal-date').value = '';
                    document.getElementById('journal-emotion').value = '开心';
                    document.getElementById('journal-situation').value = '';

                    // 重新加载日记
                    loadJournalEntries();
                    alert('日记保存成功！');
                }

                // 初始加载日记
                loadJournalEntries();
            </script>
        `
    },
    '应对策略': {
        title: '应对策略',
        content: `
            <h2>应对策略指南</h2>
            <p>这里提供了各种应对压力、焦虑和负面情绪的策略和技巧。</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="color: #6673f6; margin-bottom: 1rem;">认知重构</h3>
                    <p>识别并挑战负面思维模式，用更平衡、更现实的思考方式取代它们。</p>
                    <h4>步骤:</h4>
                    <ol>
                        <li>识别自动负面想法</li>
                        <li>评估这些想法的证据</li>
                        <li>寻找替代的、更平衡的思考方式</li>
                        <li>实践新的思考方式</li>
                    </ol>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="color: #6673f6; margin-bottom: 1rem;">问题解决</h3>
                    <p>将问题分解为可管理的部分，并制定具体的行动计划。</p>
                    <h4>步骤:</h4>
                    <ol>
                        <li>明确问题</li>
                        <li>头脑风暴可能的解决方案</li>
                        <li>评估每个解决方案的优缺点</li>
                        <li>选择并实施最佳解决方案</li>
                        <li>评估结果并调整</li>
                    </ol>
                </div>
            </div>
        `
    },
    '放松技巧': {
        title: '放松技巧',
        content: `
            <h2>放松技巧指南</h2>
            <p>这些放松技巧可以帮助你减轻身体紧张，平静心情，缓解压力。</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="color: #6673f6; margin-bottom: 1rem;">渐进式肌肉放松</h3>
                    <p>通过系统性地紧张和放松不同肌肉群来减轻身体紧张。</p>
                    <h4>步骤:</h4>
                    <ol>
                        <li>找一个安静舒适的地方坐下或躺下</li>
                        <li>从脚趾开始，用力收缩肌肉5-10秒</li>
                        <li>完全放松该肌肉群10-15秒</li>
                        <li>逐渐向上移动，依次紧张和放松小腿、大腿、臀部、腹部、胸部、手臂、肩膀、颈部和面部肌肉</li>
                        <li>完成后，保持安静和放松几分钟</li>
                    </ol>
                </div>
            </div>
        `
    },
    '心理教育': {
        title: '心理教育',
        content: `
            <h2>心理教育资源</h2>
            <p>了解心理健康知识可以帮助你更好地理解自己的情绪和行为，以及如何寻求帮助。</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="color: #6673f6; margin-bottom: 1rem;">情绪与压力</h3>
                    <p>压力是身体对需求或威胁的自然反应。适量的压力可以提高表现，但长期或过度的压力可能对身心健康造成负面影响。</p>
                    <h4>压力的生理反应:</h4>
                    <ul>
                        <li>心跳加速</li>
                        <li>呼吸急促</li>
                        <li>肌肉紧张</li>
                        <li>血压升高</li>
                        <li>出汗</li>
                    </ul>
                </div>
            </div>
        `
    }
};

// 导出工具页面对象
if (typeof module !== 'undefined') {
    module.exports = toolPages;
} else {
    window.toolPages = toolPages;
}