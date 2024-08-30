import React from "react";
import PropTypes from "prop-types";

const GeneratedText = ({ text }) => {
  return (
    <div className="text-generator-text-wrapper">
      <div dangerouslySetInnerHTML={{__html: text}} />
    </div>
  );
};

GeneratedText.propTypes = {
  text: PropTypes.string,
};

export default GeneratedText;
