import React from 'react';
import './signup.css';
import signUp from '../../../images/signupimage.svg';
import { FaRegUser } from 'react-icons/fa';
import { MdOutlineVpnKey } from 'react-icons/md';
import { AiOutlineEye, AiOutlineEyeInvisible } from 'react-icons/ai';
import { HiOutlineMail } from 'react-icons/hi';
import Alert from './Alert'

function Signup(props) {
   const {msg,show} = props
   return (
      <section className="signup-body">
         <div id="signup-content" className={props.modal ? 'active' : ''}>
            <div className="signup-container">
               <div className="left-region">
                  <h3>Eirhub</h3>
                  <div className="left-region-info-one">
                     <p>Sign up today and get in touch</p>
                  </div>

                  <div className="left-region-info-two">
                     <p> with doctors you can trust</p>
                  </div>
                  <div className="left-region-image">
                     <img src={signUp} alt="Sign-up image" />
                  </div>
               </div>
               <div className="right-region">
                  <div className="signup-form-title">
                     <h3>Create New Account</h3>
                     <p>Take control of your health today</p>
                  </div>
                  <div className="signup-form">
                     <div className="signup-form-box-names">
                        <div className="signup-form-box-name">
                           <label htmlFor="firstname"> Firstname</label>
                           <div className="signup-form-box-name-inputs">
                              <i>
                                 <FaRegUser />
                              </i>
                              <input
                                 name="firstname"
                                 type="text"
                                 id="firstname"
                                 placeholder="Enter Firstname"
                              />
                           </div>
                           {props.registerUserError && <Alert show={show} msg={msg} />}
                        </div>
                        <div className="signup-form-box-name">
                           <label htmlFor="lastname"> Lastname</label>
                           <div className="signup-form-box-name-inputs">
                              <i>
                                 <FaRegUser />
                              </i>
                              <input
                                 name="lastname"
                                 type="text"
                                 id="lastname"
                                 placeholder="Enter Lastname"
                              />
                           </div>
                        </div>
                     </div>
                     <div className="no-error-message-box">
                        <i>+ </i>
                        <p>Username must have no numbers</p>
                     </div>
                     <div className="signup-form-box">
                        <label htmlFor="date"> Date</label>
                        <div className="signup-form-box-inputs">
                           <i>
                              <FaRegUser />
                           </i>
                           <input
                              type="text"
                              name="date"
                              id="date"
                              placeholder="DD/MM/YYYY"
                              onFocus={(event) => (event.target.type = 'date')}
                              onBlur={(event) => {
                                 if (!event.target.value) {
                                    event.target.type = 'text';
                                 }
                              }}
                           />
                        </div>
                     </div>
                     <div className="no-error-message-box">
                        <i>+ </i>
                        <p>Username must have no numbers</p>
                     </div>
                     <div className="signup-form-box">
                        <label htmlFor="email"> Email</label>
                        <div className="signup-form-box-inputs">
                           <i>
                              <HiOutlineMail />
                           </i>
                           <input
                              name="email"
                              type="email"
                              id="email"
                              placeholder="Enter mail"
                           />
                        </div>
                     </div>
                     <div className="no-error-message-box">
                        <i>+ </i>
                        <p>Username must have no numbers</p>
                     </div>
                     <div className="signup-form-box">
                        <label htmlFor="passwordone"> Password</label>
                        <div className="signup-form-box-inputs">
                           <i>
                              <MdOutlineVpnKey />
                           </i>
                           <input
                              type={'password'}
                              name="password"
                              id="password1"
                              placeholder="Enter a assword"
                           />
                           <i>
                              <AiOutlineEyeInvisible />
                           </i>
                        </div>
                     </div>
                     <div className="no-error-message-box">
                        <i>+ </i>
                        <p>Username must have no numbers</p>
                     </div>

                     <div className="signup-form-box">
                        <label htmlFor="passwordconfirm">
                           {' '}
                           Confirm Password
                        </label>
                        <div className="signup-form-box-inputs">
                           <i>
                              <MdOutlineVpnKey />
                           </i>
                           <input
                              name="passwordconfirm"
                              type={'password'}
                              id="password2"
                              placeholder="Confirm your password"
                           />
                           <i>
                              <AiOutlineEyeInvisible />
                           </i>
                        </div>
                     </div>
                     <div className="no-error-message-box">
                        <i>+ </i>
                        <p>Username must have no numbers</p>
                     </div>
                     <div className="signup-form-button">
                        <input
                           type="submit"
                           id="submit-btn"
                           value="Create Account"
                           disabled={false}
                           className={'signup-btn'}
                        />
                     </div>
                     <div className="signup-form-message">
                        <p>Already have an account?</p>
                        <p id="signup-form-message-p">Login</p>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </section>
   );
}

export default Signup;
