import React from "react";
import PropTypes from "prop-types";
import WordCount from "./WordCount";

import SearchText from "./SearchText";

const Inputs = ({ wordCount, onCountChange, onSearchChange }) => {
  return (
    <div className="text-generator-inputs-wrapper">
      <WordCount wordCount={wordCount} onChange={onCountChange} />
      <SearchText onChange={onSearchChange} />
    </div>
  );
};

Inputs.propTypes = {
  wordCount: PropTypes.number,
  onCountChange: PropTypes.func,
  onSearchChange: PropTypes.func,
};

export default Inputs;
