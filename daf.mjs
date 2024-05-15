import React, { useState } from 'react';

const CharacterInfo = () => {
  const [name, setName] = useState('');
  const [race, setRace] = useState('');
  const [classType, setClassType] = useState('');
  const [alignment, setAlignment] = useState('');
  const [gender, setGender] = useState('');
  const [deity, setDeity] = useState('');
  const [image, setImage] = useState(null);

  const races = ['Human', 'Elf', 'Dwarf', 'Demon'];
  const classes = ['Crusader', 'Wizard', 'Archer', 'Darkness'];
  const alignments = ['Good', 'Neutral', 'Evil'];
  const genders = ['Male', 'Female'];

  const handleImageUpload = (event) => {
    setImage(URL.createObjectURL(event.target.files[0]));
  };

  return (
    <div className="character-info">
      <h2>Character Info</h2>
      <div className="form-group">
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="race">Race:</label>
        <select id="race" value={race} onChange={(e) => setRace(e.target.value)}>
          <option value="">-- Select Race --</option>
          {races.map((raceOption) => (
            <option key={raceOption} value={raceOption}>
              {raceOption}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="class">Class:</label>
        <select
          id="class"
          value={classType}
          onChange={(e) => setClassType(e.target.value)}
        >
          <option value="">-- Select Class --</option>
          {classes.map((classOption) => (
            <option key={classOption} value={classOption}>
              {classOption}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="alignment">Alignment:</label>
        <select
          id="alignment"
          value={alignment}
          onChange={(e) => setAlignment(e.target.value)}
        >
          <option value="">-- Select Alignment --</option>
          {alignments.map((alignmentOption) => (
            <option key={alignmentOption} value={alignmentOption}>
              {alignmentOption}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="gender">Gender:</label>
        <div className="radio-group">
          {genders.map((genderOption) => (
            <label key={genderOption}>
              <input
                type="radio"
                name="gender"
                value={genderOption}
                checked={gender === genderOption}
                onChange={(e) => setGender(e.target.value)}
              />
              {genderOption}
            </label>
          ))}
        </div>
      </div>
      <div className="form-group">
        <label htmlFor="deity">Deity (Optional):</label>
        <input
          type="text"
          id="deity"
          value={deity}
          onChange={(e) => setDeity(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="image">Character Image (Optional):</label>
        <input type="file" id="image" onChange={handleImageUpload} />
        {image && <img src={image} alt="Character Portrait" />}
      </div>
    </div>
  );
};

export default CharacterInfo;
