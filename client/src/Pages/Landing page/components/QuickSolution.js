import React from 'react';
import styles from './quickSolution.module.css';
import groupdoc from '../../../assets/TeamOfDoctors.png';
import { GiLabCoat } from 'react-icons/gi';
import { BsFillCalendar2CheckFill, BsFillStarFill } from 'react-icons/bs';
import { CgArrowLongRight } from 'react-icons/cg';

const items = [
   {
      icon: <GiLabCoat className={styles.setCol} />,
      heading: 'Find a Doctor',
      about: 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quia soluta sunt voluptates!',
   },
   {
      icon: <BsFillCalendar2CheckFill className={styles.setCol} />,
      heading: 'Schedule Appointment',
      about: 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quia soluta sunt voluptates!',
   },
   {
      icon: <BsFillStarFill className={styles.setCol} />,
      heading: 'Get a Solution',
      about: 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quia soluta sunt voluptates!',
   },
];
const QuickSolution = () => {
   return (
      <main className={styles.main}>
         <div className={styles.title}>
            <p className={styles.caption}>a quick solution for</p>
            <p className={styles.caption}>scheduling with a doctor</p>
         </div>

         {/* Display cards */}

         <div className={styles.cards}>
            {React.Children.toArray(
               items.map((item) => {
                  return (
                     <div className={styles.card}>
                        <div className={styles.icon}>{item.icon}</div>
                        <p className={styles.heading}>{item.heading}</p>
                        <p className={styles.about}>{item.about}</p>
                        <p className={styles.LearnMore}>
                           Learn more
                           <CgArrowLongRight className={styles.arrow} />
                        </p>
                     </div>
                  );
               })
            )}
         </div>

         {/* join us section */}

         <section className={styles.join_us}>
            {/* left div */}
            <div className={styles.left__div}>
               <p className={styles.firstp}>Join us!</p>
               <p className={styles.secondp}>
                  We seek to provide easy accessible services to everyone
               </p>
               <div className={styles.btn}>
                  <button className={styles.contact__btn}>Contact us</button>
               </div>
            </div>

            {/* right div with image */}
            <div className={styles.groupdocpic}>
               <img src={groupdoc} alt="" className={styles.groupdoc} />
            </div>
         </section>
      </main>
   );
};

export default QuickSolution;
