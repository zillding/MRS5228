import React, { Component, PropTypes } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import _ from 'lodash';

const data = [{
  id: 'user1',
  knn: {
    user2: 0.34,
    user6: 0.7
  }
}, {
  id: 'user2',
  knn: {
    user9: 0.34,
    user4: 0.5
  }
}];

const spanStyle = {
  marginRight: 5
};

class Table extends Component {
  render() {
    const { data, k } = this.props;
    console.log(data);
    console.log(k);

    return (
      <div>Table</div>
    );
  }
}

Table.propTypes = {
  data: PropTypes.object.isRequired,
  k: PropTypes.number.isRequired
};

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedItem: props.data[0].id
    }
  }

  _handleSelectChange(e) {
    const selectedItem = e.target.value;
    this.setState({ selectedItem });
  }

  render() {
    const { item, data, k } = this.props;
    const tableData = _.find(data, { id: this.state.selectedItem });

    return (
      <div>
        <div className="ui form">
          <div className="inline field">
            <label>Please select a {item}:</label>
            <select
              value={this.state.selectedItem}
              onChange={this._handleSelectChange.bind(this)}>
              {
                data.map(o =>
                  <option key={o.id} value={o.id}>{o.id}</option>
                )
              }
            </select>
          </div>
        </div>
        <Table data={tableData} k={k} />
      </div>
    );
  }
}

Result.propTypes = {
  item: PropTypes.string.isRequired,
  data: PropTypes.array.isRequired,
  k: PropTypes.number.isRequired
};

export class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      k: 3
    };
  }

  _handleSelectChange(e) {
    const k = parseInt(e.target.value);
    this.setState({ k });
  }

  render() {
    return (
      <div className="ui grid container">
        <div className="column">
          <h1>Recommender System</h1>
          <h3>Finding kNN</h3>
          <div className="ui form">
            <div className="inline field">
              <label>k =</label>
              <select
                value={this.state.k}
                onChange={this._handleSelectChange.bind(this)}>
                {
                  _.range(1, 10).map(value =>
                    <option key={value} value={value}>{value}</option>
                  )
                }
              </select>
            </div>
          </div>
          <Tabs>
            <TabList>
              <Tab>user-user</Tab>
              <Tab>item-item</Tab>
            </TabList>
            <TabPanel>
              <Result
                item={'user'}
                data={data}
                k={this.state.k} />
            </TabPanel>
            <TabPanel>
              <Result
                item={'movie'}
                data={data}
                k={this.state.k} />
            </TabPanel>
          </Tabs>
        </div>
      </div>
    );
  }
}
