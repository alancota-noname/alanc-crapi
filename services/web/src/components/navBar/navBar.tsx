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

import "./nav.css";

import { CUSTOM_APP_NAME } from "../../constants/constants";

import { Button, Dropdown, Menu, Avatar, Layout, Space } from "antd";
import { LogoutOutlined, DownOutlined } from "@ant-design/icons";
import React from "react";
import { useNavigate } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { logOutUserAction } from "../../actions/userActions";
import defaultProficPic from "../../assets/default_profile_pic.png";

const { Header } = Layout;

interface RootState {
  userReducer: {
    accessToken: string;
    name: string;
    isLoggedIn: boolean;
  };
  profileReducer: {
    profilePicData: string;
  };
}

interface NavbarProps extends PropsFromRedux {}

/**
 * top navigation bar that contains
 * if not logged in:
 * Login button,
 * crAPI icon,
 * if logged in :
 * dropdown to navigate to change Password or My Profile
 * dropdown alos consists the logout button
 */
const Navbar: React.FC<NavbarProps> = (props) => {
  const { logOutUser, isLoggedIn, name, profilePicData } = props;
  const navigate = useNavigate();

  const logout = () => {
    logOutUser({
      callback: () => {
        localStorage.clear();
      },
    });
  };

  const takeMenuAction = (input: { key: string }) => {
    if (input.key === "password") navigate(`/reset-password`);
    else if (input.key === "profile") navigate(`/my-profile`);
    else if (input.key === "logout") logout();
  };

  const menuSidebar = () => (
    <Menu onClick={(key) => takeMenuAction(key)}>
      <Menu.Item key="password">Change Password</Menu.Item>
      <Menu.Item key="logout">
        <LogoutOutlined /> Logout
      </Menu.Item>
    </Menu>
  );

  const takeNavigationAction = (input: { key: string }) => {
    if (input.key === "dashboard") navigate(`/`);
    else if (input.key === "shop") navigate(`/shop`);
    else if (input.key === "forum") navigate(`/forum`);
  };

  const menuNavigation = () => (
    <Menu
      onClick={(key) => takeNavigationAction(key)}
      mode="horizontal"
      theme="dark"
    >
      <Menu.Item key="dashboard">Dashboard</Menu.Item>
      <Menu.Item key="shop">Shop</Menu.Item>
      <Menu.Item key="forum">Community</Menu.Item>
    </Menu>
  );

  return (
    <Header>
      <Space className="top-nav-left">
        <div className="logo-text" onClick={() => navigate("/")}>
          {CUSTOM_APP_NAME}
        </div>
        {isLoggedIn ? menuNavigation() : <div />}
      </Space>
      {isLoggedIn ? (
        <Space className="top-nav-right">
          <div>{`Good Morning, ${name}!`}</div>
          <div className="avatarContainer">
            <Avatar
              src={profilePicData || defaultProficPic}
              className="avatar"
              size="large"
              onClick={() => navigate("/my-profile")}
            />
          </div>
          <Dropdown overlay={menuSidebar()} placement="bottomRight">
            <div className="nav-items">
              <DownOutlined />
            </div>
          </Dropdown>
        </Space>
      ) : (
        <>
          <Space className="top-nav-right">
            <Button
              className="navbar-button"
              onClick={() => {
                navigate("/login");
              }}
            >
              Login
            </Button>
            <Button
              className="navbar-button"
              onClick={() => navigate("/signup")}
            >
              Signup
            </Button>
          </Space>
        </>
      )}
    </Header>
  );
};

const mapStateToProps = (state: RootState) => ({
  accessToken: state.userReducer.accessToken,
  name: state.userReducer.name,
  isLoggedIn: state.userReducer.isLoggedIn,
  profilePicData: state.profileReducer.profilePicData,
});

const mapDispatchToProps = {
  logOutUser: logOutUserAction,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(Navbar);
