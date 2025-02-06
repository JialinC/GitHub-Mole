import React from "react";

interface TeamDisplayProps {
  teams: string[][];
  showAvatars: boolean;
}

const TeamDisplay: React.FC<TeamDisplayProps> = ({ teams, showAvatars }) => {
  return (
    <div>
      {teams.map((team, index) => (
        <div key={index} className="team-card">
          <h3>Team {index + 1}</h3>
          {team.map((memberId) => (
            <div key={memberId} className="team-member">
              {showAvatars && (
                <img
                  src={`https://api.example.com/avatar/${memberId}`}
                  alt="avatar"
                />
              )}
              <span>{memberId}</span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default TeamDisplay;
