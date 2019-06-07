import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

import 'bootstrap/dist/css/bootstrap.css';
import {
    Container, Button, Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle, Buttont, Row, Col, Table
} from 'reactstrap';

import * as tiers from './tiers.json';
import * as plans_and_features from './plans_and_features.json';

class SimplePlanTier extends React.Component {
  render() {

    const rows = [];
    let lastCategory = null;

    tiers.default.tiers.forEach((tier) => {

        rows.push(
            <Col sm="3"  key={tier.name} className="simple-plan-tier-col">
                <div className="price-card">
                    <div className="pricing-panel-wrapper">
                    <div class="pricing-panel">
                        <div className="pricing-panel-header">
                    <h6 className="pricing-panel-tier">{tier.name}</h6>
                    <h2 className="product-price product-price-lg">
                        <span className="currency">{tier.pricing.monthly.currency}</span>
                        <span className="price">{tier.pricing.monthly.price}</span>
                        <span className="period">/mo</span>
                    </h2>
                    <div class="pricing-panel-info">
                    <p className="text-light-gray">
                    <div data-alt-text="$950 billed yearly<br />Save $238/year" className="year-pricing">
                    {tier.pricing.yearly.currency}{tier.pricing.yearly.price}/mo when you <a href="#" className="yearly"> pay yearly</a>
                    </div>
                    </p>
                    </div>
                    <p></p>
                    <p>{tier.description}</p>
                    <p></p>
                    <div class="pricing-panel-footer">
                        <div class="cta-wrapper">
                    <Button className="sign-up-btn">
                        <a href={tier.call_to_action.url} className="action-link">{tier.call_to_action.text}</a>
                    </Button>
                    </div>
                    <p className="compare-plans" onClick={() => this.props.onClick()}>compare plans</p>
                    </div>
                    </div>
                    </div>
                    </div>
                </div>
            </Col>
        );
    
    });

    return (
        <Row>
                {rows}
        </Row>
    );
  }
};


class PricingPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          showDetailedPlanOveriew: false,
        };
      }

    handleClick() {
        
        // console.log("about to hide simple plan tier and show detailed plan view");
        this.setState({ showDetailedPlanOveriew: !this.state.showDetailedPlanOveriew });
    }

    render() {

        let detailRows = [];

        let categoryFeatures = [];

        tiers.default.tiers.forEach((tier) => {

            detailRows.push(
                <Col sm="2" key={tier.name} style={{textAlign: 'center'}}>
                
                    <h4 className="pricing-name">{tier.name}</h4>
                    <h2 className="product-price product-price-md">
                        <span className="currency">{tier.pricing.monthly.currency}</span>
                        <span className="price">{tier.pricing.monthly.price}</span>
                        <span className="period">/mo</span>
                    </h2>
                </Col>
            )
        });

        plans_and_features.default.categories.forEach((category) => {
            category.features.forEach((item) => {
                if(category.name == "Track & Crawl") {
                    categoryFeatures.push(
                        <div>
                            
                            <Row style={{textAlign: 'center', textAlign: 'center', margin: 'auto'}}>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.name}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Standard}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Medium}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Large}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Premium}</div>
                            </Col>
                        </Row>
                        </div>
                    )
                } else {
                    categoryFeatures.push(
                        <div>
                            
                            <h4 className="category-type-1">{category.name}</h4>
                            
                            <Row style={{textAlign: 'center', textAlign: 'center', margin: 'auto'}}>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.name}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Standard}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Medium}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Large}</div>
                            </Col>
                            <Col sm="2" className="category-feature" key = {item.name}>
                                <div>{item.values.Premium}</div>
                            </Col>
                        </Row>
                        </div>
                    ) 
                }
            })
        })

        return (
        <div className="simple-plan-tier">
            { !this.state.showDetailedPlanOveriew 
                ? 
                <Container>

                    <SimplePlanTier onClick={() => this.handleClick()}/>
                </Container>
                    : 
                <Container className="detailed-plan-view">

                    <Row>

                        <Col sm="2">

                            <h4 className="category-type-1">{plans_and_features.default.categories[0].name}</h4>
                        </Col>

                        {detailRows}
                    </Row>

                    {categoryFeatures} 

                    <p className="compare-plans" onClick={() => this.handleClick()}>Simple Plan Tier</p>

                </Container>
            }
        </div>
        );
    }
}

// ========================================

ReactDOM.render(
  <PricingPage />,
  document.getElementById('root')
);
