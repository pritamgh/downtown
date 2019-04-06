import  React, { Component } from  'react';
import Organization from './orgCRUD';

const organization = new Organization();

class OrganizationCreate extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

  handleCreate(){
      organization.createOrganization(
        {
          // "type": this.refs.type.value,
          // "org_category": this.refs.org_category.value,
          // "org_id": this.refs.org_id.value,
          // "org_password": this.refs.org_password.value,
          // "name": this.refs.name.value,
          "image": this.refs.image.value,
          // "address": this.refs.address.value,
          // "description": this.refs.description.value,
          // "website": this.refs.website.value,
          // "main_coordinator_name": this.refs.main_coordinator_name.value,
          // "main_coordinator_phone": this.refs.main_coordinator_phone.value,
          // "main_coordinator_email": this.refs.main_coordinator_email.value,
          // "sub_coordinator_name": this.refs.sub_coordinator_name.value,
          // "sub_coordinator_phone": this.refs.sub_coordinator_phone.value,
          // "sub_coordinator_email": this.refs.sub_coordinator_email.value,
          // "team": this.refs.team.value,
          // "manager_name": this.refs.manager_name.value,
          // "manager_phone": this.refs.manager_phone.value,
      }          
      ).then((result)=>{
        alert("Customer created!");
      }).catch(()=>{
        alert('There was an error! Please re-check your form.');
      });
    }

    handleSubmit(e) {
      e.preventDefault();
      // this.handleCreate();
      // e.preventDefault();
    }

    handelFile(e) {
      console.log(e.target.files[0]);
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
            <div className="form-group col-md-6">
                {/* <input className="form-control" type="text" ref='type' placeholder='type' />
                <input className="form-control" type="text" ref='org_category' placeholder='category' />
                <input className="form-control" type="text" ref='org_id' placeholder='id' />
                <input className="form-control" type="text" ref='org_password' placeholder='password' />
                <input className="form-control" type="text" ref='name' placeholder='name' />
                <input className="form-control" type="text" ref='address' placeholder='address' /> */}
                <input type="file" onChange={(e)=>this.handelFile(e)} />
                {/* <input className="form-control" type="text" ref='description' placeholder='description' />
                <input className="form-control" type="text" ref='website' placeholder='website' />
                <input className="form-control" type="text" ref='main_coordinator_name' placeholder='main co-ordinator name' />
                <input className="form-control" type="text" ref='main_coordinator_phone' placeholder='main co-ordinator phone' />
                <input className="form-control" type="text" ref='main_coordinator_email' placeholder='main co-ordinator email' />
                <input className="form-control" type="text" ref='sub_coordinator_name' placeholder='sub co-ordinator name' />
                <input className="form-control" type="text" ref='sub_coordinator_phone' placeholder='sub co-ordinator phone' />
                <input className="form-control" type="text" ref='sub_coordinator_email' placeholder='sub co-ordinator email' />
                <input className="form-control" type="text" ref='team' placeholder='team' />
                <input className="form-control" type="text" ref='manager_name' placeholder='manager name' />
                <input className="form-control" type="text" ref='manager_phone' placeholder='manager phone' /> */}
                <input className="btn btn-primary" type="submit" value="Submit" />
            </div>
            </form>
        )
    }

}

export default OrganizationCreate
