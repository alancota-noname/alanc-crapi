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

/* eslint-disable jsx-a11y/media-has-caption */
import "./profile.css";

import React, { useRef } from "react";
import { connect } from "react-redux";
import {
  Row,
  Col,
  Layout,
  Card,
  Button,
  Descriptions,
  Badge,
  Avatar,
  Dropdown,
  Menu,
  Modal,
  Form,
  Input,
} from "antd";
import { PageHeader } from "@ant-design/pro-components";
import { EditOutlined, MoreOutlined, CameraOutlined } from "@ant-design/icons";
import defaultProficPic from "../../assets/default_profile_pic.png";
import { VIDEO_NAME_REQUIRED } from "../../constants/messages";
import { useNavigate } from "react-router-dom";

const { Content } = Layout;
const { Meta } = Card;

interface UserData {
  name: string;
  email: string;
  number: string;
}

interface ProfileData {
  profilePicData?: string;
  videoData?: string;
  videoName?: string;
}

interface ProfileProps {
  hasErrored: boolean;
  errorMessage: string;
  userData: UserData;
  profileData: ProfileData;
  uploadProfilePic: (event: React.ChangeEvent<HTMLInputElement>) => void;
  uploadVideo: (event: React.ChangeEvent<HTMLInputElement>) => void;
  isVideoModalOpen: boolean;
  setIsVideoModalOpen: (isOpen: boolean) => void;
  onVideoFormFinish: (values: { videoName: string }) => void;
  shareVideoWithCommunity: () => void;
}

const Profile: React.FC<ProfileProps> = (props) => {
  const navigate = useNavigate();
  const {
    hasErrored,
    errorMessage,
    userData,
    profileData,
    uploadProfilePic,
    uploadVideo,
    isVideoModalOpen,
    setIsVideoModalOpen,
    onVideoFormFinish,
    shareVideoWithCommunity,
  } = props;

  const picInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);

  const takeVideoAction = (input: { key: string }) => {
    if (input.key === "1" && videoInputRef.current)
      videoInputRef.current.click();
    if (input.key === "2") setIsVideoModalOpen(true);
    if (input.key === "3") shareVideoWithCommunity();
  };

  const videoSideBar = () => {
    return profileData.videoData ? (
      <Menu onClick={(key) => takeVideoAction(key)}>
        <Menu.Item key="1">Change Video</Menu.Item>
        <Menu.Item key="2">Change Video Name</Menu.Item>
        <Menu.Item key="3">Share Video with Community</Menu.Item>
      </Menu>
    ) : (
      <div className="upload-video-button">
        <Button
          className="button"
          type="text"
          onClick={() => videoInputRef.current?.click()}
        >
          Upload Video
        </Button>
      </div>
    );
  };

  const renderChangePicButton = () => (
    <Button
      type="primary"
      shape="round"
      icon={<CameraOutlined />}
      size="large"
      onClick={() => picInputRef.current?.click()}
    />
  );

  const renderProfileDescription = () => (
    <Row gutter={[60, 20]}>
      <Col flex="200px">
        <Badge offset={[0, 200]} count={renderChangePicButton()}>
          <input
            type="file"
            hidden
            ref={picInputRef}
            accept="image/*"
            onChange={uploadProfilePic}
          />
          <Avatar
            shape="square"
            size={{ xs: 200, sm: 229, md: 240, lg: 260, xl: 280, xxl: 300 }}
            src={profileData.profilePicData || defaultProficPic}
          />
        </Badge>
      </Col>
      <Col flex="600px">
        <Descriptions column={1}>
          <Descriptions.Item label="Name">{userData.name}</Descriptions.Item>
          <Descriptions.Item label="Email">
            {userData.email}
            <Button
              type="primary"
              shape="round"
              className="change-email-btn"
              icon={<EditOutlined />}
              onClick={() => navigate("/change-email")}
            >
              Change email
            </Button>
          </Descriptions.Item>
          <Descriptions.Item label="Phone No.">
            {userData.number}
            <Button
              type="primary"
              shape="round"
              className="change-phone-number-btn"
              icon={<EditOutlined />}
              onClick={() => navigate("/change-phone-number")}
            >
              Change phone number
            </Button>
          </Descriptions.Item>
        </Descriptions>
      </Col>
    </Row>
  );

  const renderVideo = () => (
    <Row gutter={[60, 20]}>
      <Col span={24}>
        <>
          <video controls className="profile-video" key={profileData.videoData}>
            <source src={profileData.videoData} type="video/mp4" />
          </video>
        </>
      </Col>
    </Row>
  );

  return (
    <Layout className="page-container">
      <PageHeader title="Your Profile" className="profile-header" />
      <Content>
        <Card>
          <Meta description={renderProfileDescription()} />
        </Card>
        <PageHeader
          className="profile-header"
          title="My Personal Video"
          subTitle="Max File Size: 10MB"
          extra={[
            <Dropdown overlay={videoSideBar} key="drop-down">
              <div>
                <MoreOutlined className="more-icon" />
              </div>
            </Dropdown>,
          ]}
        />
        <input
          type="file"
          hidden
          ref={videoInputRef}
          accept="video/*"
          onChange={uploadVideo}
        />
        {profileData.videoData && (
          <Card>
            <Meta description={renderVideo()} />
          </Card>
        )}
      </Content>
      <Modal
        title="Enter new Video Name"
        visible={isVideoModalOpen}
        footer={null}
        onCancel={() => setIsVideoModalOpen(false)}
      >
        <Form
          name="basic"
          initialValues={{
            remember: true,
          }}
          onFinish={onVideoFormFinish}
        >
          <Form.Item
            name="videoName"
            initialValue={profileData.videoName}
            rules={[{ required: true, message: VIDEO_NAME_REQUIRED }]}
          >
            <Input placeholder="Car Video Name" />
          </Form.Item>
          <Form.Item>
            {hasErrored && <div className="error-message">{errorMessage}</div>}
            <Button type="primary" htmlType="submit" className="form-button">
              Change Video Name
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
};

const mapStateToProps = ({
  userReducer,
  profileReducer,
}: {
  userReducer: UserData;
  profileReducer: ProfileData;
}) => {
  return { userData: userReducer, profileData: profileReducer };
};

export default connect(mapStateToProps)(Profile);
