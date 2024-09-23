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

import React from "react";
import { Card, Row, Col, Descriptions, Spin, Layout } from "antd";
import { PageHeader } from "@ant-design/pro-components";
import { Content } from "antd/es/layout/layout";

interface Owner {
  email: string;
  number: string;
}

interface Vehicle {
  owner: Owner;
  id: string;
  vin: string;
}

interface Mechanic {
  mechanic_code: string;
  user: Owner;
}

interface Service {
  id: string;
  problem_details: string;
  created_on: string;
  vehicle: Vehicle;
  status: string;
  mechanic: Mechanic;
}

interface ServiceReportProps {
  service: Service;
}

const ServiceReport: React.FC<ServiceReportProps> = ({ service }) => {
  if (!service) {
    console.log("Service is undefined");
    return (
      <Content>
        <Spin
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
          }}
        />
      </Content>
    );
  }

  return (
    <Layout className="page-container">
      <PageHeader
        title={`Service Report: ${service.vehicle.vin} ${service.status}`}
        subTitle={service.created_on}
        className="service-report-header"
        style={{ width: "80%", margin: "auto" }}
      />
      <Card
        className="service-report-card"
        style={{ margin: "auto", width: "80%" }}
      >
        <Row gutter={[16, 16]} style={{ marginTop: "16px" }}>
          <Col>
            <Card title="Report Details" className="info-card">
              <Descriptions column={1}>
                <Descriptions.Item label="Report ID">
                  {service.id}
                </Descriptions.Item>
                <Descriptions.Item label="Report Status">
                  {service.status}
                </Descriptions.Item>
                <Descriptions.Item label="Created On">
                  {service.created_on}
                </Descriptions.Item>
                <Descriptions.Item
                  label="Problem Details"
                  style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}
                >
                  {service.problem_details}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
        <Row gutter={[16, 16]} style={{ marginTop: "16px" }}>
          <Col>
            <Card title="Assigned Mechanic" className="info-card">
              <Descriptions column={1}>
                <Descriptions.Item label="Mechanic Code">
                  {service.mechanic.mechanic_code}
                </Descriptions.Item>
                <Descriptions.Item label="Mechanic Email">
                  {service.mechanic.user.email}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
        <Row gutter={[16, 16]} style={{ marginTop: "16px" }}>
          <Col>
            <Card title="Vehicle Information" className="info-card">
              <Descriptions column={1}>
                <Descriptions.Item label="VIN">
                  {service.vehicle.vin}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
        <Row gutter={[16, 16]} style={{ marginTop: "16px" }}>
          <Col>
            <Card title="Owner Information" className="info-card">
              <Descriptions column={1}>
                <Descriptions.Item label="Email">
                  {service.vehicle.owner.email}
                </Descriptions.Item>
                <Descriptions.Item label="Phone">
                  {service.vehicle.owner.number}
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
      </Card>
    </Layout>
  );
};

export default ServiceReport;
