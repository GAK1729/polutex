import React, { Component } from 'react';
import SimpleMap from './GoogleMap';
import DatePick from './DatePicker';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import "react-datepicker/dist/react-datepicker.css";
import "./Map.css";
import { Container, Header } from "semantic-ui-react";
import Image from "../images/pm2.5.jpg";

const Coordinates = {
    'west': [[1.340381, 103.708878], [1.316184, 103.764839], [1.329181, 103.735855], [1.401475, 103.750935], [1.384057, 103.746901], [1.359087, 103.763638], [1.357374, 103.744962], [1.327345, 103.681954], [1.348447, 103.683128], [1.315841, 103.681881], [1.299365, 103.665230], [1.364631, 103.659888], [1.333569, 103.638602], [1.289543, 103.667043], [1.293233, 103.631424], [1.266659, 103.619721], [1.300006, 103.736148], [1.341108, 103.718896], [1.338579, 103.730335], [1.351997, 103.719957]],
    'north': [[1.424560, 103.760863], [1.430523, 103.755498], [1.434338, 103.762007], [1.436529, 103.748516], [1.425032, 103.770488], [1.434384, 103.769287], [1.441632, 103.772173], [1.434927, 103.787371], [1.430937, 103.801018], [1.428617, 103.803335], [1.452599, 103.799730], [1.446636, 103.803936], [1.375766, 103.860922], [1.375245, 103.878644], [1.442483, 103.819303], [1.413243, 103.897581], [1.429717, 103.857412], [1.456488, 103.821363], [1.432120, 103.796987], [1.416332, 103.827543]],
    'east': [[1.306680, 103.863027], [1.357183, 103.896238], [1.334141, 103.901193], [1.336544, 103.919046], [1.327620, 103.929174], [1.318009, 103.958185], [1.316979, 103.981531], [1.381506, 103.911665], [1.367262, 103.924368], [1.353533, 103.942735], [1.337058, 103.960932], [1.314062, 104.000929], [1.328993, 103.989599], [1.343408, 103.976038], [1.360741, 103.965051], [1.377793, 103.954353], [1.385160, 103.974272], [1.353926, 103.992468], [1.323379, 104.010321], [1.356672, 104.024225]],
    'south': [[1.310628, 103.840542], [1.322984, 103.803464], [1.316634, 103.825865], [1.312687, 103.791791], [1.312859, 103.808098], [1.310628, 103.827324], [1.305200, 103.850842], [1.299508, 103.858395], [1.296505, 103.870755], [1.299471, 103.899615], [1.286428, 103.783572], [1.297926, 103.813784], [1.295695, 103.843139], [1.282480, 103.774989], [1.279048, 103.797820], [1.277332, 103.820651], [1.274243, 103.850005], [1.268751, 103.835757], [1.251418, 103.821168], [1.259461, 103.838162], [1.240754, 103.838677]],
    'central': [[1.359322, 103.778964], [1.353031, 103.794338], [1.353717, 103.808929], [1.354747, 103.824808], [1.353889, 103.847381], [1.349083, 103.873469], [1.344328, 103.894165], [1.344242, 103.875110], [1.343212, 103.865326], [1.332916, 103.854854], [1.331886, 103.866828], [1.326952, 103.875024], [1.323176, 103.881290], [1.329612, 103.882363], [1.334074, 103.879273], [1.338321, 103.875926], [1.322318, 103.878715], [1.329011, 103.881891], [1.331628, 103.849147]],
    'national': [[0, 0]]
}

export default class PM extends Component {
    constructor(props) {
        super(props);
        this.state = {
            date: "",
            data: ""
        }
        this.onChangeDate = this.onChangeDate.bind(this);
        this.changeMap = this.changeMap.bind(this);
    }

    onChangeDate(newDate) {
        this.setState({
            date: newDate
        })
    }

    changeMap() {
        axios
            .post(`http://localhost:5000/pm`, {
                date: this.state.date
            })
            .then((res) => {
                const locations = {
                    west: { 'latitude': 1.35735, 'longitude': 103.7 },
                    east: { 'latitude': 1.35735, 'longitude': 103.94 },
                    central: { 'latitude': 1.35735, 'longitude': 103.82 },
                    south: { 'latitude': 1.29587, 'longitude': 103.82 },
                    north: { 'latitude': 1.41803, 'longitude': 103.82 },
                    national: { 'latitude': 0, 'longitude': 0 }
                }
                var resData = [];
                Object.keys(res.data).map(key => {
                    resData.push({
                        lat: locations[key]['latitude'],
                        lng: locations[key]['longitude'],
                        weight: res.data[key]
                    })
                })
                Object.keys(res.data).map(key => {
                    Coordinates[key].forEach(coordinate => resData.push({
                        lat: coordinate[0], lng: coordinate[1],
                        weight: res.data[key]
                    }))
                })
                this.setState({
                    data: res.data
                });
                this.refs.map.onMap(resData);
            })
    }

    render() {
        return (
            <div>
                <div className="container" style={{color: "white"}}><h1>PM2.5 National Assessment</h1></div>
                <Container text style={{
                    padding: "10%", fontSize: "200%", marginTop: "5%", marginBottom: "5%",
                    boxShadow: "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    backgroundColor: "white", borderRadius: "20px"
                }}> 
                <img src={Image} style={{width: "100%"}}/>
                    <Header>Particulate Matter (PM2.5)</Header>
                    PM2.5 refers to atmospheric particulate matter (PM) that have a diameter of less than 2.5 micrometers,
                    which is about 3% the diameter of a human hair. Commonly written as PM2.5, particles in this category 
                    are so small that they can only be detected with an electron microscope. They are even smaller than 
                    their counterparts PM10, which are particles that are 10 micrometres or less, and are also called fine particles. 
                </Container>
                <Container text style={{
                    padding: "10%", fontSize: "200%", marginTop: "5%", marginBottom: "5%",
                    boxShadow: "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    backgroundColor: "white", borderRadius: "20px"
                }}>
                <SimpleMap ref="map" />
                <DatePick function={this.onChangeDate} />
                <Button variant="primary" onClick={this.changeMap}>Submit</Button>
                </Container>
                {this.state.data ? <div className="container" id="shadowText">
                    <h1>PM2.5 Values</h1>
                    {Object.keys(this.state.data).map(key => <h2>{`${key.charAt(0).toUpperCase() + key.slice(1)}: ${this.state.data[key]}`}</h2>)}
                </div> : <div></div>
                }
            </div>
        );
    }
}