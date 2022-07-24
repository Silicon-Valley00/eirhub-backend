import React, { useState, useRef } from 'react';
import Signup from './components/Signup';
import Login from './components/Login';
import DoctorSignup from './components/DoctorSignup';
import DoctorLogin from './components/DoctorLogin';
import axios from 'axios';

// Database configuration
const api = axios.create({
   baseURL: 'http://127.0.0.1:5000/',
});

function Registration(props) {
   // User sign in refs for patients
   const loginEmail = useRef();
   const loginPassword = useRef();

   // User sign in refs for doctors
   const loginEmailDoctor = useRef();
   const loginPasswordDoctor = useRef();

   // User sign up refs for patients
   const signupFirstname = useRef();
   const signupLastname = useRef();
   const signupEmail = useRef();
   const signupPassword = useRef();
   const signupPasswordconfirm = useRef();
   const signupDate = useRef();
   const signupHospitalCode = useRef();

   // Handles error state of input boxes
   const [loginEmailError, setloginEmailError] = useState(null);
   const [loginPasswordError, setLoginPasswordError] = useState(null);

   const [loginEmailErrorDoctor, setloginEmailErrorDoctor] = useState(null);
   const [loginPasswordErrorDoctor, setLoginPasswordErrorDoctor] =
      useState(null);

   const [registerNameError, setRegisterNameError] = useState(null);
   const [registerDateError, setRegisterDateError] = useState(null);
   const [registerHospitalCodeError, setRegisterHospitalCodeError] =
      useState(null);
   const [registerEmailError, setRegisterEmailError] = useState(null);
   const [registerPasswordOneError, setRegisterPasswordOneError] =
      useState(null);
   const [registerPasswordTwoError, setRegisterPasswordTwoError] =
      useState(null);

   // Handles error messages of input boxes
   const [registerNameErrorMessage, setRegisterNameErrorMessage] = useState('');
   const [registerDateErrorMessage, setRegisterDateErrorMessage] = useState('');
   const [
      registerHospitalCodeErrorMessage,
      setRegisterHospitalCodeErrorMessage,
   ] = useState('');
   const [registerEmailErrorMessage, setRegisterEmailErrorMessage] =
      useState('');
   const [registerPasswordOneErrorMessage, setRegisterPasswordOneErrorMessage] =
      useState('');
   const [registerPasswordTwoErrorMessage, setRegisterPasswordTwoErrorMessage] =
      useState('');
   // Patient
   const [loginEmailErrorMessage, setloginEmailErrorMessage] = useState('');
   const [loginPasswordErrorMessage, setLoginPasswordErrorMessage] =
      useState('');
   // Doctors
   const [loginEmailErrorMessageDoctor, setloginEmailErrorMessageDoctor] =
      useState('');
   const [loginPasswordErrorMessageDoctor, setLoginPasswordErrorMessageDoctor] =
      useState('');

   const pattern = /^[a-zA-Z ]+$/;
   const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

   // Functions below check user credentials in each form input
   function handleloginEmail() {
      let enteredloginName = loginEmail.current.value;

      if (enteredloginName === '') {
         setloginEmailError(true);
         setloginEmailErrorMessage('Email required');
      } else if (enteredloginName.match(emailPattern)) {
         setloginEmailError(false);
      } else {
         setloginEmailError(true);
         setloginEmailErrorMessage('Email format not valid');
      }
   }

   function handleLoginPassword() {
      let enteredloginPassword = loginPassword.current.value;

      if (enteredloginPassword === '') {
         setLoginPasswordErrorMessage('Password required');
         setLoginPasswordError(true);
      } else if (enteredloginPassword.length < 8) {
         setLoginPasswordErrorMessage(
            'Password must be at least 8 characters long'
         );

         setLoginPasswordError(true);
      } else {
         setLoginPasswordError(false);
      }
   }
   function handleloginEmailDoctor() {
      let enteredloginName = loginEmailDoctor.current.value;

      if (enteredloginName === '') {
         setloginEmailErrorDoctor(true);
         setloginEmailErrorMessageDoctor('Email required');
      } else if (enteredloginName.match(emailPattern)) {
         setloginEmailErrorDoctor(false);
      } else {
         setloginEmailErrorDoctor(true);
         setloginEmailErrorMessageDoctor('Email format not valid');
      }
   }

   function handleLoginPasswordDoctor() {
      let enteredloginPassword = loginPasswordDoctor.current.value;

      if (enteredloginPassword === '') {
         setLoginPasswordErrorMessageDoctor('Password required');
         setLoginPasswordErrorDoctor(true);
      } else if (enteredloginPassword.length < 8) {
         setLoginPasswordErrorMessageDoctor(
            'Password must be at least 8 characters long'
         );

         setLoginPasswordErrorDoctor(true);
      } else {
         setLoginPasswordErrorDoctor(false);
      }
   }

   // Functions below check user credentials in login form
   function handleRegisterUser() {
      let enteredSignUpFirstname = signupFirstname.current.value;
      let enteredSignUpLastname = signupLastname.current.value;

      if (enteredSignUpFirstname === '' || enteredSignUpLastname === '') {
         setRegisterNameErrorMessage('Full name required');
         setRegisterNameError(true);
      } else if (
         enteredSignUpFirstname.match(pattern) !== 1 &&
         enteredSignUpLastname.match(pattern) !== 1
      ) {
         setRegisterNameError(false);
      } else {
         setRegisterNameErrorMessage('Name must have only letters');

         setRegisterNameError(true);
      }
   }

   function handleRegisterEmail() {
      let enteredSignUpEmail = signupEmail.current.value;

      if (enteredSignUpEmail === '') {
         setRegisterEmailErrorMessage('Email required');
         setRegisterEmailError(true);
      } else if (enteredSignUpEmail.match(emailPattern)) {
         setRegisterEmailError(false);
      } else {
         setRegisterEmailErrorMessage('Email format not valid');
         setRegisterEmailError(true);
      }
   }
   function handleRegisterDate() {
      let enteredSignUpDate = signupDate.current.value;

      if (enteredSignUpDate === '') {
         setRegisterDateErrorMessage('Date required');
         setRegisterDateError(true);
      } else {
         setRegisterDateError(false);
      }
   }

   function handleRegisterHospitalCode() {
      let enteredSignupHospitalCode = signupHospitalCode.current.value;

      if (enteredSignupHospitalCode === '') {
         setRegisterHospitalCodeErrorMessage('Hospital code required');
         setRegisterHospitalCodeError(true);
      } else {
         setRegisterHospitalCodeError(false);
      }
   }

   function handleRegisterPassword() {
      let enteredSignUpPassword = signupPassword.current.value;

      if (enteredSignUpPassword === '') {
         setRegisterPasswordOneErrorMessage('Password required');
         setRegisterPasswordOneError(true);
      } else if (enteredSignUpPassword.length < 8) {
         setRegisterPasswordOneErrorMessage(
            'Password must be at least 8 characters long'
         );
         setRegisterPasswordOneError(true);
      } else if (enteredSignUpPassword.search(/[0-9]/) === -1) {
         setRegisterPasswordOneErrorMessage(
            'Password must contain at least a number'
         );
         setRegisterPasswordOneError(true);
      } else if (enteredSignUpPassword.search(/[a-z]/) === -1) {
         setRegisterPasswordOneErrorMessage(
            'Password must contain at least a lowercase character'
         );
         setRegisterPasswordOneError(true);
      } else if (enteredSignUpPassword.search(/[A-Z]/) === -1) {
         setRegisterPasswordOneErrorMessage(
            'Password must contain at least an uppercase character'
         );
         setRegisterPasswordOneError(true);
      } else if (enteredSignUpPassword.search(/[,./;%^&*<>?:|]/) === -1) {
         setRegisterPasswordOneErrorMessage(
            'Password must contain at least a special character'
         );
         setRegisterPasswordOneError(true);
      } else {
         setRegisterPasswordOneError(false);
      }
   }

   function handleRegisterPasswordConfirm() {
      let enteredSignUpPasswordconfirm = signupPasswordconfirm.current.value;
      let enteredSignUpPassword = signupPassword.current.value;

      if (enteredSignUpPasswordconfirm === '') {
         setRegisterPasswordTwoErrorMessage('Confirm password required');
         setRegisterPasswordTwoError(true);
      } else if (enteredSignUpPassword !== enteredSignUpPasswordconfirm) {
         setRegisterPasswordTwoErrorMessage('Passwords do not match');
         setRegisterPasswordTwoError(true);
      } else {
         setRegisterPasswordTwoError(false);
      }
   }

   // function handles submittion of user data to database
   async function submitUserCredentialsHandler() {
      // User entered credentials
      let enteredloginEmail = loginEmail.current.value;
      let enteredloginPassword = loginPassword.current.value;

      let enteredloginEmailDoctor = loginEmailDoctor.current.value;
      let enteredloginPasswordDoctor = loginPasswordDoctor.current.value;

      let enteredSignUpFirstname = signupFirstname.current.value;
      let enteredSignUpLastname = signupLastname.current.value;
      let enteredSignUpDate = signupDate.current.value;
      let enteredSignUpEmail = signupEmail.current.value;
      let enteredSignUpPassword = signupPassword.current.value;
      let enteredSignUpPasswordconfirm = signupPasswordconfirm.current.value;

      let enteredSignupHospitalCode = signupHospitalCode.current.value;

      // Below codes check which modal form is open to take user credentials
      if (props.modalLogin) {
         //checks if the patient login form modal is opened
         // prepares credentials for submition
         const loginPatientData = {
            email: enteredloginEmail,
            password: enteredloginPassword,
         };
         console.log(loginPatientData);
         submitCredentials('patient/login', loginPatientData);
      } else if (props.modalSignup) {
         //checks if the patient signup form modal is opened
         // prepares credentials for submition
         const signupPatientData = {
            firstname: enteredSignUpFirstname,
            lastname: enteredSignUpLastname,
            dateOfBirth: enteredSignUpDate,
            user_email: enteredSignUpEmail,
            password: enteredSignUpPassword,
         };

         console.log(signupPatientData);
         console.log('start');
         submitCredentials('patient/signup', signupPatientData);
         console.log('end');
      } else if (props.modalSignupDoctor) {
         //checks if the doctor signup form modal is opened
         // prepares credentials for submittion
         const signupDoctorData = {
            firstname: enteredSignUpFirstname,
            lastname: enteredSignUpLastname,
            hospitalCode: enteredSignupHospitalCode,
            user_email: enteredSignUpEmail,
            password: enteredSignUpPassword,
         };

         console.log(signupDoctorData);
         console.log('start');
         submitCredentials('doctorsignup', signupDoctorData);
         console.log('end');
      } else if (props.modalLoginDoctor) {
         //checks if the doctor login form modal is opened
         // prepares credentials for submittion
         const loginDoctorData = {
            email: enteredloginEmailDoctor,
            password: enteredloginPasswordDoctor,
         };

         console.log(loginDoctorData);
         console.log('start');
         submitCredentials('doctorlogin', loginDoctorData);
         console.log('end');
      }
   }

   // Function submits data to database via an api
   async function submitCredentials(path, data) {
      //Function takes path and data to make request
      axios({
         method: 'post',
         url: `http://127.0.0.1:5000/${path}`,
         headers: {
            'Access-Control-Allow-Origin': '*',
         },
         data: { data },
      })
         .then((response) => {
            //Checks if response is ok
            if (response.status === 200) {
               //checks details of response
               console.log('good', response);
            }
         })
         //catches all errorr when response is not ok, 404 included
         .catch((error) => {
            if (error.response) {
               console.log('data', error.response.data);
            } else if (error.request) {
               console.log('request', error.request);
            } else {
               console.log(error);
               console.log('message', error.message);
            }
         });
   }

   return (
      <>
         <Login
            modalLoginDoctor={props.modalLoginDoctor}
            handleModalSignupDoctor={props.handleModalSignupDoctor}
            handleModalsClose={props.handleModalsClose}
            submitUserCredentialsHandler={submitUserCredentialsHandler}
            loginEmail={loginEmail}
            handleloginEmail={handleloginEmail}
            handleLoginPassword={handleLoginPassword}
            loginPassword={loginPassword}
            loginEmailError={loginEmailError}
            loginPasswordError={loginPasswordError}
            loginEmailErrorMessage={loginEmailErrorMessage}
            loginPasswordErrorMessage={loginPasswordErrorMessage}
         />
         <DoctorLogin
            modalLogin={props.modalLogin}
            handleModalSignup={props.handleModalSignup}
            handleModalsClose={props.handleModalsClose}
            submitUserCredentialsHandler={submitUserCredentialsHandler}
            loginEmailDoctor={loginEmailDoctor}
            handleloginEmailDoctor={handleloginEmailDoctor}
            handleLoginPasswordDoctor={handleLoginPasswordDoctor}
            loginPasswordDoctor={loginPasswordDoctor}
            loginEmailErrorDoctor={loginEmailErrorDoctor}
            loginPasswordErrorDoctor={loginPasswordErrorDoctor}
            loginEmailErrorMessageDoctor={loginEmailErrorMessageDoctor}
            loginPasswordErrorMessageDoctor={loginPasswordErrorMessageDoctor}
         />

         <Signup
            modalSignup={props.modalSignup}
            handleModalLogin={props.handleModalLogin}
            handleModalsClose={props.handleModalsClose}
            submitUserCredentialsHandler={submitUserCredentialsHandler}
            signupFirstname={signupFirstname}
            signupLastname={signupLastname}
            signupEmail={signupEmail}
            signupPassword={signupPassword}
            signupDate={signupDate}
            signupPasswordconfirm={signupPasswordconfirm}
            registerNameError={registerNameError}
            registerEmailError={registerEmailError}
            registerDateError={registerDateError}
            registerPasswordOneError={registerPasswordOneError}
            registerPasswordTwoError={registerPasswordTwoError}
            registerNameErrorMessage={registerNameErrorMessage}
            registerEmailErrorMessage={registerEmailErrorMessage}
            registerDateErrorMessage={registerDateErrorMessage}
            registerPasswordOneErrorMessage={registerPasswordOneErrorMessage}
            registerPasswordTwoErrorMessage={registerPasswordTwoErrorMessage}
            handleRegisterUser={handleRegisterUser}
            handleRegisterEmail={handleRegisterEmail}
            handleRegisterDate={handleRegisterDate}
            handleRegisterPassword={handleRegisterPassword}
            handleRegisterPasswordConfirm={handleRegisterPasswordConfirm}
         />
         {/* <DoctorSignup
            modalSignupDoctor={props.modalSignupDoctor}
            handleModalLoginDoctor={props.handleModalLoginDoctor}
            handleModalsClose={props.handleModalsClose}
            submitUserCredentialsHandler={submitUserCredentialsHandler}
            signupFirstname={signupFirstname}
            signupLastname={signupLastname}
            signupEmail={signupEmail}
            signupPassword={signupPassword}
            signupHospitalCode={signupHospitalCode}
            signupPasswordconfirm={signupPasswordconfirm}
            registerNameError={registerNameError}
            registerEmailError={registerEmailError}
            registerHospitalCodeError={registerHospitalCodeError}
            registerPasswordOneError={registerPasswordOneError}
            registerPasswordTwoError={registerPasswordTwoError}
            registerNameErrorMessage={registerNameErrorMessage}
            registerEmailErrorMessage={registerEmailErrorMessage}
            registerHospitalCodeErrorMessage={registerHospitalCodeErrorMessage}
            registerPasswordOneErrorMessage={registerPasswordOneErrorMessage}
            registerPasswordTwoErrorMessage={registerPasswordTwoErrorMessage}
            handleRegisterUser={handleRegisterUser}
            handleRegisterEmail={handleRegisterEmail}
            handleRegisterHospitalCode={handleRegisterHospitalCode}
            handleRegisterPassword={handleRegisterPassword}
            handleRegisterPasswordConfirm={handleRegisterPasswordConfirm}
         /> */}
      </>
   );
}
export default Registration;
