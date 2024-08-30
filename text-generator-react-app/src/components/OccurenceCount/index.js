import React from "react";
import PropTypes from "prop-types";
import { Typography } from "antd";

const { Title } = Typography;

const OccurenceCount = ({ count }) => {
  return <Title level={5}>Found {count} occurrences</Title>;
};

OccurenceCount.propTypes = {
  count: PropTypes.string,
};

export default OccurenceCount;
