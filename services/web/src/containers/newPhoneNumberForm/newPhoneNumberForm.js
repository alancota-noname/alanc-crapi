/*
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { Modal } from "antd";
import React from "react";

import PropTypes from "prop-types";
import { connect } from "react-redux";
import responseTypes from "../../constants/responseTypes";
import { SUCCESS_MESSAGE } from "../../constants/messages";
import NewPhoneNumberForm from "../../components/newPhoneNumberForm/newPhoneNumberForm";
import { changePhoneNumberAction } from "../../actions/userActions";

const NewPhoneNumberFormContainer = (props) => {
  const { accessToken, oldPhoneNumber, onPhoneNumberChange } = props;

  const [hasErrored, setHasErrored] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState("");

  const callback = (res, data) => {
    if (res === responseTypes.SUCCESS) {
      Modal.success({
        title: SUCCESS_MESSAGE,
        content: data,
        onOk: () => props.setCurrentStep(props.currentStep + 1),
      });
    } else {
      setHasErrored(true);
      setErrorMessage(data);
    }
  };

  const onFinish = (values) => {
    props.changePhoneNumber({
      ...values,
      callback,
      accessToken,
      old_number: oldPhoneNumber,
    });
  };

  return (
    <NewPhoneNumberForm
      onFinish={onFinish}
      hasErrored={hasErrored}
      errorMessage={errorMessage}
      onPhoneNumberChange={onPhoneNumberChange}
    />
  );
};

const mapStateToProps = ({ userReducer: { accessToken, number } }) => {
  return { accessToken, oldPhoneNumber: number };
};

const mapDispatchToProps = {
  changePhoneNumber: changePhoneNumberAction,
};

NewPhoneNumberFormContainer.propTypes = {
  oldPhoneNumber: PropTypes.string,
  accessToken: PropTypes.string,
  changePhoneNumber: PropTypes.func,
  currentStep: PropTypes.number,
  setCurrentStep: PropTypes.func,
  onPhoneNumberChange: PropTypes.func,
};

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(NewPhoneNumberFormContainer);
