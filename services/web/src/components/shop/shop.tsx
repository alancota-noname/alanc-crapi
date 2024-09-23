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

import "./styles.css";
import React from "react";
import { connect, ConnectedProps } from "react-redux";
import {
  Row,
  Col,
  Layout,
  Descriptions,
  Card,
  Button,
  Avatar,
  Form,
  Modal,
  Input,
} from "antd";
import { PageHeader } from "@ant-design/pro-components";
import {
  PlusOutlined,
  OrderedListOutlined,
  ShoppingCartOutlined,
} from "@ant-design/icons";
import { COUPON_CODE_REQUIRED } from "../../constants/messages";
import { useNavigate } from "react-router-dom";

const { Content } = Layout;
const { Meta } = Card;

interface Product {
  id: string;
  name: string;
  price: number;
  image_url: string;
}

interface ShopProps extends PropsFromRedux {
  products: Product[];
  availableCredit: number;
  isCouponFormOpen: boolean;
  setIsCouponFormOpen: (isOpen: boolean) => void;
  hasErrored: boolean;
  errorMessage: string;
  onFinish: (values: any) => void;
  prevOffset: number | null;
  nextOffset: number | null;
  onOffsetChange: (offset: number | null) => void;
  onBuyProduct: (product: Product) => void;
}

const ProductAvatar: React.FC<{ image_url: string }> = ({ image_url }) => (
  <Avatar
    shape="square"
    className="product-avatar"
    size={250}
    src={image_url}
  />
);

const ProductDescription: React.FC<{
  product: Product;
  onBuyProduct: (product: Product) => void;
}> = ({ product, onBuyProduct }) => (
  <>
    <PageHeader title={`${product.name}, $${product.price}`} />
    <Button
      type="primary"
      shape="round"
      icon={<ShoppingCartOutlined />}
      size="large"
      key="buy-product"
      className="buy-btn"
      onClick={() => onBuyProduct(product)}
    >
      Buy
    </Button>
  </>
);

const Shop: React.FC<ShopProps> = (props) => {
  const navigate = useNavigate();
  const {
    products,
    availableCredit,
    isCouponFormOpen,
    setIsCouponFormOpen,
    hasErrored,
    errorMessage,
    onFinish,
    prevOffset,
    nextOffset,
    onOffsetChange,
    onBuyProduct,
  } = props;

  return (
    <Layout className="page-container">
      <PageHeader
        className="page-header"
        title="Shop"
        onBack={() => navigate("/dashboard")}
        extra={[
          <Button
            type="primary"
            shape="round"
            icon={<PlusOutlined />}
            size="large"
            key="add-coupons"
            onClick={() => setIsCouponFormOpen(true)}
          >
            Add Coupons
          </Button>,
          <Button
            type="primary"
            shape="round"
            icon={<OrderedListOutlined />}
            size="large"
            onClick={() => navigate("/past-orders")}
            key="past-orders"
          >
            Past Orders
          </Button>,
        ]}
      />
      <Descriptions column={1} className="balance-desc">
        <Descriptions.Item label="Available Balance">
          {`$${availableCredit}`}
        </Descriptions.Item>
      </Descriptions>
      <Content>
        <Row gutter={[40, 40]}>
          {products.map((product) => (
            <Col span={8} key={product.id}>
              <Card
                className="product-card"
                cover={<ProductAvatar image_url={product.image_url} />}
              >
                <Meta
                  description={
                    <ProductDescription
                      product={product}
                      onBuyProduct={onBuyProduct}
                    />
                  }
                />
              </Card>
            </Col>
          ))}
        </Row>
        <Row justify="center" className="pagination">
          <Button
            type="primary"
            shape="round"
            size="large"
            onClick={() => onOffsetChange(prevOffset)}
            key="prev-button"
            disabled={prevOffset === null}
          >
            Previous
          </Button>
          <Button
            type="primary"
            shape="round"
            size="large"
            key="next-button"
            onClick={() => onOffsetChange(nextOffset)}
            disabled={!nextOffset}
          >
            Next
          </Button>
        </Row>
      </Content>
      <Modal
        title="Enter Coupon Code"
        open={isCouponFormOpen}
        footer={null}
        onCancel={() => setIsCouponFormOpen(false)}
      >
        <Form
          name="basic"
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
        >
          <Form.Item
            name="couponCode"
            rules={[{ required: true, message: COUPON_CODE_REQUIRED }]}
          >
            <Input placeholder="Coupon Code" />
          </Form.Item>
          <Form.Item>
            {hasErrored && <div className="error-message">{errorMessage}</div>}
            <Button type="primary" htmlType="submit" className="form-button">
              Validate
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
};

interface RootState {
  shopReducer: {
    accessToken: string;
    availableCredit: number;
    products: Product[];
    prevOffset: number | null;
    nextOffset: number | null;
  };
}

const mapStateToProps = (state: RootState) => {
  const { accessToken, availableCredit, products, prevOffset, nextOffset } =
    state.shopReducer;
  return { accessToken, availableCredit, products, prevOffset, nextOffset };
};

const connector = connect(mapStateToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(Shop);
