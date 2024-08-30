import React from "react";
import PropTypes from "prop-types";
import { SearchOutlined } from "@ant-design/icons";
import { Input } from "antd";

const SearchText = ({ onChange }) => {
  return (
    <Input
      placeholder="Find in text"
      onChange={(e) => {
        onChange(e.target.value);
      }}
      suffix={<SearchOutlined />}
    />
  );
};

SearchText.propTypes = {
  onChange: PropTypes.func,
};

export default SearchText;
