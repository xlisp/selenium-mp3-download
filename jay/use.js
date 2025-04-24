// 获取所有音乐列表
const allMusic = getMusicList();
console.log('所有音乐:', allMusic);

// 搜索周杰倫的歌曲
const jayMusic = searchMusic('周杰倫');
console.log('周杰倫的歌曲:', jayMusic);

// 按发布日期排序（最新的先显示）
const latestMusic = sortByReleaseDate(false);
console.log('最新音乐:', latestMusic);

// 获取缩略图信息
const thumbnails = getThumbInfo();
console.log('缩略图信息:', thumbnails);

// 获取发布年份统计
const yearStats = getReleaseYearStats();
console.log('年份统计:', yearStats);

// 监听列表变化
const observer = observeMusicList((updatedList) => {
    console.log('列表已更新:', updatedList);
});

// ======== 
// 获取所有歌曲名称的简单函数
function getSongTitles() {
    // 获取所有带有 data-list-li-li 类的 li 元素
    const musicItems = document.querySelectorAll('li.data-list-li-li');
    
    // 提取歌曲名称并返回数组
    return Array.from(musicItems)
        .map(li => {
            // 获取歌曲标题元素 (在 span 标签内)
            const titleSpan = li.querySelector('h3 a span.am-margin-sm');
            // 返回标题文本，并去除空白字符
            return titleSpan ? titleSpan.textContent.trim() : '';
        })
        // 过滤掉空标题
        .filter(title => title);
}

// 使用方法
const songTitles = getSongTitles();
console.log('歌曲列表:');
songTitles.forEach((title, index) => {
    console.log(`${index + 1}. ${title}`);
});

