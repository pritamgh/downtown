import  React, { Component } from  'react';
import Organization from './orgCRUD';

const organization = new Organization();

class OrganizationList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            organizations: [],
        };
    }

    componentDidMount() {
        var  self  =  this;
        organization.getOrganizationList().then(function (result) {
            console.log(result);
            self.setState({ organizations:  result})
        });
    }

    render() {
        return (
            <div className="table-responsive-sm">
                <table className="table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Type</th>
                            <th>Category</th>
                            <th>Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.organizations.map(item => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.type}</td>
                                <td>{item.org_category}</td>
                                <td>{item.name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    }

}

export default OrganizationList;