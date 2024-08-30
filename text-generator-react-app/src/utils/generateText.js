import wordList from 'mnemonic-words';

export default (wordCount) => {
  var words = [];

  for (let i = 0; i < wordCount; i++) {
    const randomIndex = Math.floor(Math.random() * wordList.length);
    words.push(wordList[randomIndex]);
  }

  return words.join(" ");
};
