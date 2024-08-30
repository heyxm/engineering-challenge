import React, { useState, useEffect } from "react";
import { Layout, Typography } from "antd";

import Inputs from "../Inputs";
import OccurenceCount from "../OccurenceCount";
import GeneratedText from "../GeneratedText";
import { generateText } from "../../utils";

const { Header, Content } = Layout;
const { Title } = Typography;

const countOccurence = (text, search) => {
  if (!search || !text) return 0;
  return [...text.matchAll(search)].length;
};

const TextGenerator = () => {
  const [wordCount, setWordCount] = useState(0);
  const [search, setSearch] = useState("");
  const [generatedText, setGeneratedText] = useState("");
  const [occurenceCount, setOccurenceCount] = useState(0);

  useEffect(() => {
    var text = generateText(wordCount);
    setGeneratedText(text);
    setOccurenceCount(countOccurence(text, search));
  }, [wordCount]);

  useEffect(() => {
    setOccurenceCount(countOccurence(generatedText, search));
  }, [search]);

  const getHTMLText = (text) =>
    !!search ? text.replaceAll(search, `<mark>${search}</mark>`) : text;

  return (
    <Layout className="text-generator-layout">
      <Header className="text-generator-header">
        <Title level={2}>Text generator</Title>
      </Header>
      <Content>
        <Inputs
          wordCount={wordCount}
          onCountChange={setWordCount}
          onSearchChange={setSearch}
        />
        <OccurenceCount count={occurenceCount} />
        <GeneratedText
          wordCount={wordCount}
          text={getHTMLText(generatedText)}
        />
      </Content>
    </Layout>
  );
};

export default TextGenerator;
