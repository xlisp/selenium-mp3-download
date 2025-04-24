// https://song.corp.com.tw/singer.aspx?singer=%E5%91%A8%E6%9D%B0%E5%80%AB
// 查找所有符合条件的 li 元素
function getMusicList() {
    // 获取所有带有 data-list-li-li 类的 li 元素
    const musicItems = document.querySelectorAll('li.data-list-li-li');
    
    // 将查询结果转换为数组并提取信息
    return Array.from(musicItems).map(li => {
        // 获取基本信息
        const id = li.id;
        const thumbnailImg = li.querySelector('img');
        const titleElement = li.querySelector('h3 a span');
        const infoElements = li.querySelectorAll('.am-text-sm');
        
        // 提取歌手和专辑信息
        const singerElement = infoElements[0]?.querySelector('a');
        const albumElement = infoElements[1]?.querySelector('a');
        const releaseDateElement = infoElements[2];
        
        // 构建返回对象
        return {
            id: id,
            thumbnail: thumbnailImg?.src || '',
            thumbnailAlt: thumbnailImg?.alt || '',
            title: titleElement?.textContent?.trim() || '',
            singer: {
                name: singerElement?.textContent || '',
                link: singerElement?.href || ''
            },
            album: {
                name: albumElement?.textContent || '',
                link: albumElement?.href || ''
            },
            releaseDate: releaseDateElement?.textContent.replace('發行：', '').trim() || '',
            // 获取完整链接
            link: li.querySelector('h3 a')?.href || ''
        };
    });
}

// 使用方法
const musicList = getMusicList();
console.log(musicList);

// 按发布日期排序
function sortByReleaseDate(ascending = true) {
    const items = getMusicList();
    return items.sort((a, b) => {
        const dateA = new Date(a.releaseDate);
        const dateB = new Date(b.releaseDate);
        return ascending ? dateA - dateB : dateB - dateA;
    });
}

// 搜索功能
function searchMusic(keyword) {
    const items = getMusicList();
    const lowercaseKeyword = keyword.toLowerCase();
    
    return items.filter(item => 
        item.title.toLowerCase().includes(lowercaseKeyword) ||
        item.singer.name.toLowerCase().includes(lowercaseKeyword) ||
        item.album.name.toLowerCase().includes(lowercaseKeyword)
    );
}

// 监听列表变化
function observeMusicList(callback) {
    const observer = new MutationObserver((mutations) => {
        callback(getMusicList());
    });
    
    const container = document.querySelector('ul'); // 替换为实际的容器选择器
    if (container) {
        observer.observe(container, {
            childList: true,
            subtree: true
        });
    }
    
    return observer;
}

// 示例：获取特定歌手的所有歌曲
function getSongsBySinger(singerName) {
    const items = getMusicList();
    return items.filter(item => 
        item.singer.name.toLowerCase() === singerName.toLowerCase()
    );
}

// 获取缩略图信息
function getThumbInfo() {
    const items = getMusicList();
    return items.map(item => ({
        id: item.id,
        title: item.title,
        thumbnailUrl: item.thumbnail,
        altText: item.thumbnailAlt
    }));
}

// 提取发布年份统计
function getReleaseYearStats() {
    const items = getMusicList();
    const yearStats = {};
    
    items.forEach(item => {
        const year = item.releaseDate.split('-')[0];
        yearStats[year] = (yearStats[year] || 0) + 1;
    });
    
    return yearStats;
}

