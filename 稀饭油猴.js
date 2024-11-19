// ==UserScript==
// @name         稀饭动漫视频下载
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  提取动态加载的视频链接并通过美化后的GUI按钮进行跳转，窗口可缩放，显示链接详情
// @author       CMB
// @match        https://dick.xfani.com/watch/*.html
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    let isVideoUrlFound = false;
    let videoUrl;

    // 每秒检查一次
    const intervalId = setInterval(() => {
        const scriptElement = document.querySelector('script[type="text/javascript"]');
        if (scriptElement &&!isVideoUrlFound) {
            const scriptText = scriptElement.textContent;
            const jsonStartIndex = scriptText.indexOf('{');
            const jsonEndIndex = scriptText.lastIndexOf('}');
            if (jsonStartIndex!== -1 && jsonEndIndex!== -1) {
                const jsonData = scriptText.substring(jsonStartIndex, jsonEndIndex + 1);
                const playerData = JSON.parse(jsonData);
                videoUrl = playerData.url;
                console.log(videoUrl);

                isVideoUrlFound = true;
                clearInterval(intervalId);

                // 创建GUI界面元素
                createDownloadUI(videoUrl);
            }
        }
    }, 1000);


    function createDownloadUI(videoUrl) {
        // 创建窗口容器
        const container = document.createElement('div');
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.width = '300px';
        container.style.height = '150px';
        container.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        container.style.color = 'white';
        container.style.padding = '10px';
        container.style.borderRadius = '10px';
        container.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'space-between';
        container.style.zIndex = '9999';

        // 显示视频链接
        const linkText = document.createElement('p');
        linkText.textContent = '视频链接：';
        linkText.style.margin = '0';
        linkText.style.textAlign = 'center';
        container.appendChild(linkText);

        const linkInput = document.createElement('input');
        linkInput.type = 'text';
        linkInput.value = videoUrl;
        linkInput.style.width = '95%';
        linkInput.style.textAlign = 'center';
        linkInput.style.border = 'none';
        linkInput.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        linkInput.style.color = 'white';
        linkInput.style.padding = '5px';
        linkInput.readOnly = true;
        container.appendChild(linkInput);

        // 跳转按钮
        const jumpButton = document.createElement('button');
        jumpButton.textContent = '下载视频';
        jumpButton.style.marginTop = '10px';
        jumpButton.style.padding = '8px 15px';
        jumpButton.style.backgroundColor = '#4CAF50';
        jumpButton.style.color = 'white';
        jumpButton.style.border = 'none';
        jumpButton.style.borderRadius = '5px';
        jumpButton.style.cursor = 'pointer';
        jumpButton.addEventListener('click', () => {
            window.open(videoUrl, '_blank');
        });
        container.appendChild(jumpButton);

        // 添加到页面
        document.body.appendChild(container);

        // 监听键盘按键 "-" 缩小窗口
        document.addEventListener('keydown', (e) => {
            if (e.key === '-') {
                if (container.style.height === '30px') {
                    // 恢复窗口
                    container.style.height = '150px';
                    container.style.width = '300px';
                } else {
                    // 缩小窗口
                    container.style.height = '30px';
                    container.style.width = '100px';
                }
            }
        });
    }
})();