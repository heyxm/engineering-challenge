import React from "react";
import PropTypes from "prop-types";
import { InputNumber } from "antd";

const WordCount = ({ wordCount, onChange }) => {
  return (
    <InputNumber
      min={0}
      value={wordCount}
      onChange={onChange}
      addonBefore="Word count"
      parser={(value) => value.replace(/\D/g, "")}
    />
  );
};

WordCount.propTypes = {
  wordCount: PropTypes.number,
  onChange: PropTypes.func,
};

export default WordCount;
