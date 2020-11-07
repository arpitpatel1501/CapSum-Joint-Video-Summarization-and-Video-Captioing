import React from 'react';
import {Button,Grid} from '@material-ui/core/';
//import Upload from './Upload';
import Login from './Login';
import MainPage from './MainPage';

class App extends React.Component {
  constructor(props){
    super(props);
    this.state={
      user:{
        email:null,
        fname:null,
        lname:null,
        img:null
      },
      loggedIn:false,
    }
  }
  componentDidMount(){
      if(localStorage.getItem('email')!==null){
          let email=localStorage.getItem('email');
          let fname=localStorage.getItem('fname');
          let lname=localStorage.getItem('lname');
          let img=localStorage.getItem('img');
          this.setState({user:{email:email,fname:fname,lname:lname,img:img}});
          this.setState({loggedIn:true})
      }
  }


  render(){
    return(
      <div >
        <div style={{}}>
        { this.state.loggedIn ? null : 
          <Login onLogin={(email,fname,lname,img)=>{
            this.setState({user:{email,fname,lname,img}});
            if(email!==null){
              this.setState({loggedIn:true})
              localStorage.setItem("email", email);
              localStorage.setItem("fname", fname);
              localStorage.setItem("lname", lname);
              localStorage.setItem("img", img);
            //   fetch('http://127.0.0.1:5000/login',{method:'POST',headers:{"Content-Type": "application/json"},body:JSON.stringify({user:this.state.user})})
              fetch('http://34.68.228.193:8080/login',{method:'POST',headers:{"Content-Type": "application/json"},body:JSON.stringify({user:this.state.user})})
            }
          }} 
          />
        }

        </div>
        <div>
          {this.state.loggedIn ? <MainPage user={this.state.user} /> : null}
        </div>
      </div>
    )
  }
}
export default App;
