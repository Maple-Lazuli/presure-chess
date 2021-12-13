import React from 'react';
import 'semantic-ui-css/semantic.min.css'




const pieces = {
    '0': {
        name: 'Empty Space',
        icon: 'square full icon',
        color: 'space',
    },
    '1': {
        name: 'black Rook',
        icon: 'chess rook icon',
        color: 'red'
    },
    '2': {
        name: 'black Knight',
        icon: 'chess knight icon',
        color: 'red'
    },
    '3': {
        name: 'black Bishop',
        icon: 'chess bishop icon',
        color: 'red'
    },
    '4': {
        name: 'black Queen',
        icon: 'chess queen icon',
        color: 'red'
    },
    '5': {
        name: 'black King',
        icon: 'chess king icon',
        color: 'red'
    },
    '6': {
        name: 'black Bishop Colored',
        icon: 'chess bishop icon',
        color: 'red'
    },
    '9': {
        name: 'black Pawn',
        icon: 'chess pawn icon',
        color: 'red'
    },
    '11': {
        name: 'white Rook',
        icon: 'chess rook icon',
        color: 'teal'
    },
    '12': {
        name: 'white Knight',
        icon: 'chess knight icon',
        color: 'teal'
    },
    '13': {
        name: 'white Bishop',
        icon: 'chess bishop icon',
        color: 'teal'
    },
    '14': {
        name: 'white Queen',
        icon: 'chess queen icon',
        color: 'teal'
    },
    '15': {
        name: 'white King',
        icon: 'chess king icon',
        color: 'teal'
    },
    '16': {
        name: 'white Bishop Colored',
        icon: 'chess bishop icon',
        color: 'teal'
    },
    '10': {
        name: 'white Pawn',
        icon: 'chess pawn icon',
        color: 'teal'
    },
}

const color = (base, weight) => {
    if (base < 0) {
        return `rgba(255,0,0,${weight})`
    } else if (base > 0) {
        return `rgba(0,0,255,${weight})`
    } else {
        return ""
    }
}

const chessIndex = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

const Square = (props) => {
    return (
        <div index={`${props.index}`} style={{ backgroundColor: `${props.colorVal}` }}>
            <i className="huge icons" index={`${props.index}`}>
                <i className="big circle outline icon space" index={`${props.index}`}></i>
                <i className={`${pieces[props.position].icon} ${pieces[props.position].color}  piece`} index={`${props.index}`}></i>
            </i>
            <span className='indexIndicator'>
                {props.index}
            </span>
            <span className='chessPosition'>
                {chessIndex[parseInt(props.index)]}
            </span>
        </div>
    );
};
export default Square;